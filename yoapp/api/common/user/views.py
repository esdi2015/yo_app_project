from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.contrib.auth import get_user_model
from django.core import serializers

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_auth.models import TokenModel
from rest_auth.app_settings import create_token

import httplib2
from googleapiclient.discovery import build
from oauth2client.client import AccessTokenCredentials
import facebook
from google.oauth2 import id_token
from google.auth.transport import requests

from ...views import custom_api_response
from .serializers import CustomUserSerializer, LoginSerializer, UserIsExistsSerializer

from ...account.serializers import ProfileSerializer
from account.models import Profile
from common.utils import ROLES

import re
from django.core.files.base import ContentFile
from urllib.parse import urlparse
from urllib.request import urlopen

from ...utils import ERROR_API

UserModel = get_user_model()


class Logout(APIView):
    #queryset = UserModel.objects.all()

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
    #queryset = UserModel.objects.all()

    def get(self, request, format=None):
        serializer = CustomUserSerializer(request.user)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_200_OK)


class UserIsExists(APIView):
    permission_classes = (AllowAny,)
    #queryset = UserModel.objects.all()

    def post(self, request, format=None):
        serializer = UserIsExistsSerializer(data=request.data)
        if serializer.is_valid():
            return Response(custom_api_response(serializer=serializer), status=status.HTTP_200_OK)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        #queryset = UserModel.objects.filter(role='CUSTOMER').all()
        #user = get_object_or_404(queryset, pk=pk)
        user = UserModel.objects.filter(pk=pk).all()
        serializer = CustomUserSerializer(user, many=True)
        response = Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        return response

    def list(self, request, *args, **kwargs):
        users = UserModel.objects.filter(role='MANAGER', creator_id=request.user.pk).all()
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #serializer = self.get_serializer(queryset, many=True)
        serializer = CustomUserSerializer(users, many=True)

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


from django_rest_passwordreset.views import ResetPasswordRequestToken
class UserResetPasswordRequestToken(ResetPasswordRequestToken):
    pass

user_reset_password_request_token = UserResetPasswordRequestToken.as_view()


@api_view(['POST'])
@permission_classes(())
def reset_password_request(request):
    from django_rest_passwordreset.views import reset_password_request_token
    content = reset_password_request_token
    print (content)
    #return Response(custom_api_response(content={'detail': 'testttt 1111'}), status=status.HTTP_200_OK)
    return Response(content.as_view())


@api_view(['POST'])
@permission_classes(())
def reset_password_confirm(request):
    return Response(custom_api_response(content={'detail': 'testttt 2222'}), status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes(())
def register_view(request):
    # registration handler
    if request.user.is_authenticated == True:
        # error = {"detail": "You must have to log out first"}
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            token = create_token(TokenModel, user, login_serializer)

            django_login(request, user)
            content = {'token': token.key, 'email': user.email, 'id': user.id}
            #return Response(custom_api_response(serializer), status=status.HTTP_201_CREATED)
            return Response(custom_api_response(login_serializer, content), status=status.HTTP_200_OK)
        else:
            return Response(custom_api_response(login_serializer), status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(())
def login_view(request):
    if request.user.is_authenticated == True:
        # error = {"detail": "You must have to log out first"}
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token = create_token(TokenModel, user, serializer)
        django_login(request, user)
        profile = get_profile_data(user.id)
        content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': False, 'profile': profile}
        return Response(custom_api_response(serializer, content), status=status.HTTP_200_OK)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)



def get_profile_data(user_id):
    user_profile = Profile.objects.filter(user_id=user_id).all()
    profile_serializer = ProfileSerializer(instance=user_profile, many=True)
    profile = profile_serializer.data
    return profile



@api_view(['POST'])
@permission_classes(())
def google_oauth(request):
    if request.user.is_authenticated:
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        #return Response({"detail": "You must have to log out first"})
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    token=request.data['id_token']

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "440629677274-jkrfq9i93asr3j2du8t0jqggsegh3tk8.apps.googleusercontent.com")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
    except ValueError:
        error = {"detail": ERROR_API['111'][1]}
        error_codes = [ERROR_API['111'][0]]
        # return Response({"error":"Unable to login via google account, wrong issuer"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

    last_name = idinfo['family_name']
    first_name = idinfo['given_name']
    email = idinfo['email']
    photo = idinfo['picture']

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
        user = UserModel(email=email, last_name=last_name, first_name=first_name)
        user.save()
        user.profile.photo.save(name, content, save = True)
        user.save()
        first_login = True

    token = create_login_token(user)
    profile = get_profile_data(user.id)
    content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': first_login, 'profile': profile}
    return Response(custom_api_response(content=content), status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes(())
# def test(request):
#     photo = "https://i.imgur.com/gkjCJVf.jpg"
#
#     name = urlparse(photo).path.split('/')[-1]
#     # wrap your file content
#     content = ContentFile(urlopen(photo).read())
#
#
#     print(name)
#     print(content)
#
#     user = UserModel(email='dsadsa@com.com', last_name='fdsfds', first_name='fdsfdsfs')
#     user.save()
#     user.profile.photo.save(name, content, save=True)
#     user.save()
#
#     return Response('ok',status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes(())
def facebook_oauth(request):

    def create_login_token(user):
        serializer = LoginSerializer()
        token = create_token(TokenModel, user, serializer)
        return token

    if request.user.is_authenticated == True:
        # error = {"detail": "You must have to log out first"}
        error = {"detail": ERROR_API['109'][1]}
        error_codes = [ERROR_API['109'][0]]
        # return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)
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
            # return Response({'error': 'already registered'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
        except UserModel.DoesNotExist:
            user = UserModel(email=email, last_name=last_name, first_name=first_name, fb_id=fb_id)
            user.save()
            user.profile.photo.save(name,content,save=True)
            first_login = True

    if user.fb_id == fb_id:
        token = create_login_token(user)
        profile = get_profile_data(user.id)
        content = {'token': token.key, 'email': user.email, 'id': user.id, 'first_login': first_login, 'profile': profile}
        return Response(custom_api_response(content=content), status=status.HTTP_200_OK)
    else:
        error = {"detail": ERROR_API['112'][1]}
        error_codes = [ERROR_API['112'][0]]
        # return Response({'error': 'Unable to login via facebook account, wrong id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)





