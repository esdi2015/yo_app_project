from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
# from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ...views import custom_api_response
from .serializers import ShopSerializer, ShopListSerializer


ShopModel = apps.get_model('yomarket', 'Shop')


class ShopViewSet(viewsets.ModelViewSet):
    queryset = ShopModel.objects.all()
    serializer_class = ShopSerializer
    # permission_classes = (AllowAny,)

    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('title', 'address', )
    filter_fields = ('manager_id', )
    ordering_fields = '__all__'

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), AllowAny(), ] # AllowAny(), - remove it later !!!

    def retrieve(self, request, pk=None):
        queryset = ShopModel.objects.filter(pk=pk).all()
        serializer = ShopSerializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        if (request.user.is_authenticated == True) and (request.user.role == 'OWNER'):
            queryset = ShopModel.objects.filter(user_id=request.user.pk).all()
        else:
            queryset = ShopModel.objects.all()

        queryset = self.filter_queryset(queryset)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #serializer = self.get_serializer(queryset, many=True)
        serializer = ShopListSerializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        request.data['user_id'] = request.user.pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data['user_id'] = request.user.pk
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)