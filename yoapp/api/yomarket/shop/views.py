from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter

from api.views import CustomPagination, prepare_paginated_response
from ...views import custom_api_response
from .serializers import ShopSerializer, ShopListSerializer, ShopCreateUpdateSerializer
from api.utils import ERROR_API

from history.utils import history_view_event

ShopModel = apps.get_model('yomarket', 'Shop')


class ShopListFilter(FilterSet):
    category_ids = CharFilter(method='filter_category_ids')
    manager_ids = CharFilter(method='filter_manager_ids')
    city_ids = CharFilter(method='filter_city_ids')

    class Meta:
        model = ShopModel
        fields = ('manager_id', 'code_type', 'city_id', 'categories__id',
                  'category_ids', 'manager_ids', 'city_ids')

    def filter_category_ids(self, queryset, name, value):
        if value:
            queryset = queryset.filter(categories__id__in=value.strip().split(',')).all()
        return queryset

    def filter_manager_ids(self, queryset, name, value):
        if value:
            queryset = queryset.filter(manager_id__in=value.strip().split(',')).all()
        return queryset

    def filter_city_ids(self, queryset, name, value):
        if value:
            queryset = queryset.filter(city_id__in=value.strip().split(',')).all()
        return queryset


class ShopViewSet(viewsets.ModelViewSet):
    queryset = ShopModel.objects.all()
    serializer_class = ShopSerializer
    pagination_class = CustomPagination
    filter_class = ShopListFilter

    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('title', 'address', 'description', )
    ordering_fields = ('image', 'title', 'description', 'address', 'city__city_name', 'manager',
                       'phone', 'outer_link', 'social_link', 'schedule__title', 'code_type')

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]

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
        if not queryset.exists():
            error = {"detail": ERROR_API['251'][1]}
            error_codes = [ERROR_API['251'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        paginate = prepare_paginated_response(self, request, queryset)
        if paginate:
            return Response(custom_api_response(content=paginate.content, metadata=paginate.metadata), status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.serializer_class = ShopCreateUpdateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.save(user_id=request.user.pk)
        headers = self.get_success_headers(serializer.data)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ShopCreateUpdateSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=False):
            if request.user.role == 'MANAGER':
                serializer.save()
            elif request.user.role=='OWNER':
                serializer.save(user_id=request.user.pk)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        else:
            return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)