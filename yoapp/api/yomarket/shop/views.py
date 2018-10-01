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

from history.utils import history_view_event

ShopModel = apps.get_model('yomarket', 'Shop')


class ShopViewSet(viewsets.ModelViewSet):
    queryset = ShopModel.objects.all()
    serializer_class = ShopSerializer
    # permission_classes = (AllowAny,)

    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('title', 'address', 'description', )
    filter_fields = ('manager_id', 'code_type', 'city_id', 'categories__id')
    #ordering_fields = '__all__'
    ordering_fields = ('image', 'title', 'description', 'address', 'city__city_name', 'manager',
                       'phone', 'outer_link', 'social_link', 'schedule__title', 'code_type')

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), AllowAny(), ] # AllowAny(), - remove it later !!!

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        history_view_event(obj=instance,user=request.user)
        serializer = self.get_serializer(instance)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ShopListSerializer
        queryset = self.get_queryset()

        if (request.user.is_authenticated == True) and (request.user.role == 'OWNER'):
            queryset = self.queryset.filter(user_id=request.user.pk).all()
        elif (request.user.is_authenticated == True) and (request.user.role == 'MANAGER'):
            queryset = self.queryset.filter(manager_id=request.user.pk).all()
        else:
            queryset = self.queryset

        queryset = self.filter_queryset(queryset)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(user_id=request.user.pk)
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

        serializer.save(user_id=request.user.pk)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)