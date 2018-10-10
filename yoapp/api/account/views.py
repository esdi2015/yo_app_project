from django.apps import apps
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_auth.models import TokenModel

from ..views import custom_api_response
from .serializers import ProfileSerializer, ProfilePhotoSerializer, ProfileUpdateSerializer
from history.utils import history_profile_update_event

ProfileModel = apps.get_model('user_account', 'Profile')
UserModel = get_user_model()


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfileModel.objects.all()

    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        profile_data = serializer.data
        token = TokenModel.objects.filter(user_id=request.user.pk).first()
        profile_data['token'] = str(token)
        #return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        return Response(custom_api_response(content=profile_data), status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ProfileUpdateSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        history_profile_update_event(user=request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        #self.perform_update(serializer)

        # if getattr(instance, '_prefetched_objects_cache', None):
        #     # If 'prefetch_related' has been applied to a queryset, we need to
        #     # forcibly invalidate the prefetch cache on the instance.
        #     instance._prefetched_objects_cache = {}

        serializer.save(user_id=request.user.pk)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


class ProfilePhotoView(generics.CreateAPIView):
    queryset = ProfileModel.objects.all()

    serializer_class = ProfilePhotoSerializer
    permission_classes = (IsAuthenticated, )
    allowed_methods = ('POST', )

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance, serializer.validated_data)
            serializer = self.get_serializer(instance)
            return Response(custom_api_response(content=serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)