from django.apps import apps
from rest_framework import generics
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_auth.models import TokenModel

from ..views import custom_api_response
from .serializers import ProfileSerializer


ProfileModel = apps.get_model('user_account', 'Profile')


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
        profile_data['region'] = None
        profile_data['interests'] = None
        #return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        return Response(custom_api_response(content=profile_data), status=status.HTTP_200_OK)

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

        serializer.save(user_id=request.user.pk)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)