from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.contrib.auth import get_user_model

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_auth.models import TokenModel
from rest_auth.app_settings import create_token

import facebook
from google.oauth2 import id_token
from google.auth.transport import requests

from ...views import custom_api_response
from .serializers import CustomUserSerializer, LoginSerializer, UserIsExistsSerializer, RegisterUserSerializer

from ...account.serializers import ProfileSerializer
from account.models import Profile
from common.utils import ROLES

import re
from django.core.files.base import ContentFile
from urllib.parse import urlparse
from urllib.request import urlopen

from ...utils import ERROR_API

from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from rest_framework import parsers, renderers, status
from rest_framework.response import Response
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.signals import reset_password_token_created, pre_password_reset, post_password_reset
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from yomarket.models import Shop
from api.views import CustomPagination, prepare_paginated_response
from yoapp import cipher

User = get_user_model()
UserModel = get_user_model()


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        content = {"detail": "Successfully user logged out"}
        return Response(custom_api_response(None, content), status=status.HTTP_200_OK)


class UserMe(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = CustomUserSerializer(request.user)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_200_OK)


class UserIsExists(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = UserIsExistsSerializer(data=request.data)
        if serializer.is_valid():
            return Response(custom_api_response(serializer=serializer), status=status.HTTP_200_OK)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering_fields = ('username', 'first_name', 'last_name', 'email')

    def retrieve(self, request, pk=None):
        user = UserModel.objects.filter(pk=pk).all()
        serializer = self.get_serializer(user, many=True)
        response = Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        return response

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(role='MANAGER', creator_id=request.user.pk).all()
        queryset = self.filter_queryset(queryset)

        if not queryset.exists():
            error = {"detail": ERROR_API['122'][1]}
            error_codes = [ERROR_API['122'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        paginate = prepare_paginated_response(self, request, queryset)
        if paginate:
            return Response(custom_api_response(content=paginate.content, metadata=paginate.metadata), status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self_user = request.user
        request.data['creator_id'] = self_user.pk
        request.data['role'] = 'MANAGER'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)



class UserResetPasswordConfirm(ResetPasswordConfirm):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        password=cipher.decrypt(password)
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            # return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)
            error = {"detail": ERROR_API['113'][1]}
            error_codes = [ERROR_API['113'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            # return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)
            error = {"detail": ERROR_API['114'][1]}
            error_codes = [ERROR_API['114'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        # change users password
        if reset_password_token.user.has_usable_password():
            pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

        # Delete all password reset tokens for this user
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        return Response({'status': 'OK'})


class UserResetPasswordRequestToken(ResetPasswordRequestToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # before we continue, delete all existing expired tokens
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # datetime.now minus expiry hours
        now_minus_expiry_time = timezone.now() - timedelta(hours=password_reset_token_validation_time)

        # delete all tokens where created_at < now - 24 hours
        ResetPasswordToken.objects.filter(created_at__lte=now_minus_expiry_time).delete()

        # find a user by email address (case insensitive search)
        users = User.objects.filter(email__iexact=email)

        active_user_found = False

        # iterate over all users and check if there is any user that is active
        # also check whether the password can be changed (is useable), as there could be users that are not allowed
        # to change their password (e.g., LDAP user)
        for user in users:
            if user.is_active and user.has_usable_password():
                active_user_found = True

        # No active user found, raise a validation error
        if not active_user_found:
            # raise ValidationError({
            #     'email': ValidationError(
            #         _("There is no active user associated with this e-mail address or the password can not be changed"),
            #         code='invalid')}
            # )
            error = {"detail": ERROR_API['104'][1]}
            error_codes = [ERROR_API['104'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        # last but not least: iterate over all users that are active and can change their password
        # and create a Reset Password Token and send a signal with the created token
        for user in users:
            if user.is_active and user.has_usable_password():
                # define the token as none for now
                token = None

                # check if the user already has a token
                if user.password_reset_tokens.all().count() > 0:
                    # yes, already has a token, re-use this token
                    token = user.password_reset_tokens.all()[0]
                else:
                    # no token exists, generate a new token
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent=request.META['HTTP_USER_AGENT'],
                        ip_address=request.META['REMOTE_ADDR']
                    )
                # send a signal that the password token was created
                # let whoever receives this signal handle sending the email for the password reset
                reset_password_token_created.send(sender=self.__class__, reset_password_token=token)
        # done
        return Response({'status': 'OK'})


user_reset_password_confirm = UserResetPasswordConfirm.as_view()
user_reset_password_request_token = UserResetPasswordRequestToken.as_view()


@api_view(['POST'])
@permission_classes(())
def register_view(request):
    # registration handler
    if request.user.is_authenticated == True:
        # "You must have to log out first"
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    is_user_exists = UserModel.objects.filter(email=request.data['email']).all()
    if is_user_exists:
        error = {"detail": ERROR_API['103'][1]}
        error_codes = [ERROR_API['103'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        new_profile_data = {'date_birth': serializer.validated_data['date_birth'] if 'date_birth' in serializer.validated_data else None,
                            'phone': serializer.validated_data['phone'] if 'phone' in serializer.validated_data else '',
                            'subscribe': serializer.validated_data['subscribe'] if 'subscribe' in serializer.validated_data else False}

        if 'date_birth' in serializer.validated_data:
            del serializer.validated_data['date_birth']
        if 'phone' in serializer.validated_data:
            del serializer.validated_data['phone']
        if 'subscribe' in serializer.validated_data:
            del serializer.validated_data['subscribe']

        instance = serializer.save()
        instance_id = instance.id
        user_profile = Profile.objects.filter(user_id=instance_id).first()
        profile_serialiser = ProfileSerializer(instance=user_profile, data=new_profile_data)
        if profile_serialiser.is_valid():
            profile_serialiser.save()

        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            token = create_token(TokenModel, user, login_serializer)
            django_login(request, user)
            profile = get_profile_data(user.id, request)
            content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': True,
                   'first_name': user.first_name, 'last_name': user.last_name, 'profile': profile}
            return Response(custom_api_response(login_serializer, content), status=status.HTTP_200_OK)
        else:
            return Response(custom_api_response(login_serializer), status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(())
def login_view(request):
    serializer_class = LoginSerializer
    if request.user.is_authenticated == True:
        # "You must have to log out first"
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token = create_token(TokenModel, user, serializer)
        django_login(request, user)
        profile = get_profile_data(user.id, request)
        content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': False,
                   'first_name': user.first_name, 'last_name': user.last_name, 'profile': profile}
        return Response(custom_api_response(serializer, content), status=status.HTTP_200_OK)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)



def get_profile_data(user_id, request=None):
    user_profile = Profile.objects.filter(user_id=user_id).all()
    profile_serializer = ProfileSerializer(instance=user_profile, many=True)
    profile = profile_serializer.data
    if request:
        if profile[0]['photo']:
            profile[0]['photo'] = request.build_absolute_uri(profile[0]['photo'])
    if profile:
        return profile[0]
    else:
        return {}



@api_view(['POST'])
@permission_classes(())
def google_oauth(request):
    if request.user.is_authenticated:
        # "You must have to log out first"
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    token=request.data['id_token']

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "440629677274-jkrfq9i93asr3j2du8t0jqggsegh3tk8.apps.googleusercontent.com")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
    except ValueError:
        # "Unable to login via google account, wrong issuer"
        error = {"detail": ERROR_API['111'][1]}
        error_codes = [ERROR_API['111'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    last_name = idinfo['family_name']
    first_name = idinfo['given_name']
    email = idinfo['email']
    photo = idinfo['picture']
    google_id = idinfo['sub']

    first_login = False

    photo = re.sub(r'/s\d\d-c/',r'/s500-c/',photo)
    name = urlparse(photo).path.split('/')[-1]
    content = ContentFile(urlopen(photo).read())

    def create_login_token(user):
        serializer = LoginSerializer()
        token = create_token(TokenModel, user, serializer)
        return token

    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        try:
             user = UserModel.objects.get(google_id=google_id)
             error = {"detail": ERROR_API['110'][1]}
             error_codes = [ERROR_API['110'][0]]
             return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
        except UserModel.DoesNotExist:
            user = UserModel(email=email, last_name=last_name, first_name=first_name, google_id=google_id)
            user.save()
            user.profile.photo.save(name, content, save = True)
            user.save()
            first_login = True

    if user.google_id == google_id:
        token = create_login_token(user)
        profile = get_profile_data(user.id, request)
        content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': first_login,
               'first_name': user.first_name, 'last_name': user.last_name, 'profile': profile}
        return Response(custom_api_response(content=content), status=status.HTTP_200_OK)
    else:
        error = {"detail": ERROR_API['120'][1]}
        error_codes = [ERROR_API['120'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes(())
def facebook_oauth(request):

    def create_login_token(user):
        serializer = LoginSerializer()
        token = create_token(TokenModel, user, serializer)
        return token

    if request.user.is_authenticated == True:
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    access_token = request.data['access_token']
    email = request.data['email']

    graph = facebook.GraphAPI(access_token)
    args = {'fields': 'id,email,birthday,gender,first_name,last_name,picture.height(500)'}
    profile = graph.get_object('me', **args)

    first_name = profile.get('first_name')
    last_name = profile.get('last_name')
    gender = profile.get('gender')
    birthday = profile.get('birthday')
    fb_id = profile.get('id')

    first_login = False

    photo = profile.get('picture',{}).get('data',{}).get('url',{})
    name = urlparse(photo).path.split('/')[-1]+'fb.jpg'
    content = ContentFile(urlopen(photo).read())

    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        try:
             user = UserModel.objects.get(fb_id=fb_id)
             error = {"detail": ERROR_API['110'][1]}
             error_codes = [ERROR_API['110'][0]]
             return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
        except UserModel.DoesNotExist:
            user = UserModel(email=email, last_name=last_name, first_name=first_name, fb_id=fb_id)
            user.save()
            user.profile.photo.save(name,content,save=True)
            first_login = True
            user = UserModel.objects.get(email=email)

    if user.fb_id == fb_id:
        token = create_login_token(user)
        profile = get_profile_data(user.id, request)
        content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': first_login,
                   'first_name': user.first_name, 'last_name': user.last_name, 'profile': profile}
        return Response(custom_api_response(content=content), status=status.HTTP_200_OK)
    else:
        error = {"detail": ERROR_API['120'][1]}
        error_codes = [ERROR_API['120'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes(())
def free_managers_view(request):
    if request.user.is_authenticated == False:
        error = {"detail": ERROR_API['115'][0]}
        error_codes = [ERROR_API['115'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    users = UserModel.objects.filter(role='MANAGER', creator_id=request.user.pk).all()

    users_list=list()

    for user in users:
         try:
             shop=Shop.objects.get(manager=user)
         except Shop.DoesNotExist:
             users_list.append(user)

    serializer = CustomUserSerializer(users_list, many=True)
    return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


import twitter
from twitter import TwitterError

@api_view(['POST'])
@permission_classes(())
def twitter_login(request):

    def create_login_token(user):
        serializer = LoginSerializer()
        token = create_token(TokenModel, user, serializer)
        return token

    if request.user.is_authenticated == True:
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    access_token = request.data['access_token']
    access_token_secret = request.data['access_token_secret']

    email = request.data['email']


    api = twitter.Api(consumer_key='P9xv5rNHFY4rYcOr8Fg2kH0TH',
                      consumer_secret='bSRFJAWwgDrR2TWnX3Z9mxwtyPgtAvKmseu9vQ4XjFP66Bd2fB',
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)

    try:
        twitter_user = api.VerifyCredentials(include_email=True)
    except TwitterError:
        error = {"detail": ERROR_API['121'][1]}
        error_codes = [ERROR_API['121'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    twitter_id = twitter_user.id_str

    first_login = False


    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        try:
            user = UserModel.objects.get(twitter_id=twitter_id)
            error = {"detail": ERROR_API['110'][1]}
            error_codes = [ERROR_API['110'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
        except UserModel.DoesNotExist:
            user = UserModel(email=email, twitter_id=twitter_id)
            user.save()
            first_login = True


    if user.twitter_id == twitter_id:
        token = create_login_token(user)
        profile = get_profile_data(user.id, request)
        content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': first_login,'profile': profile}
        return Response(custom_api_response(content=content), status=status.HTTP_200_OK)
    else:
        error = {"detail": ERROR_API['120'][1]}
        error_codes = [ERROR_API['120'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)


