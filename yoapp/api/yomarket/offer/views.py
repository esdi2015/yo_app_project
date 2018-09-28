from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
import datetime

from ...views import custom_api_response
from .serializers import OfferSerializer

from rest_framework.pagination import LimitOffsetPagination
from statistic.utlis import count_shown
from history.utils import history_view_event
from ...utils import ERROR_API


OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')
UserModel = get_user_model()


class OfferListView(generics.ListCreateAPIView):
    #queryset = OfferModel.objects.all()

    serializer_class = OfferSerializer
    #permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('description', 'title')
    filter_fields = ('category_id', 'shop_id', 'discount_type', 'offer_type', )
    #ordering_fields = '__all__'
    #ordering_fields = ('shop')
    ordering_fields = ('shop__title', 'category__category_name', 'title', 'image',
                       'short_description', 'price', 'offer_type', 'expire', )


    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]

    def get_queryset(self):
        #print (self.request.user.role)
        queryset = OfferModel.objects.all()
        #queryset = OfferModel.objects.filter(expire__gte=datetime.datetime.now()).all()
        #queryset = OfferModel.objects.filter(price=10).all()
        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            try:
                offer_type = self.request.GET['offer_type']
            except Exception as e:
                offer_type = None

            if offer_type == 'DAILY':
                error = {"detail": ERROR_API['205'][1]}
                error_codes = [ERROR_API['205'][0]]
            elif offer_type == 'REGULAR':
                error = {"detail": ERROR_API['206'][1]}
                error_codes = [ERROR_API['206'][0]]
            else:
                error = {"detail": ERROR_API['204'][1]}
                error_codes = [ERROR_API['204'][0]]

            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated == True:
            if request.user.role == 'OWNER':
                shops = ShopModel.objects.filter(user_id=request.user.pk).all()
            elif request.user.role == 'MANAGER':
                shops = ShopModel.objects.filter(manager_id=request.user.pk).all()

            if request.user.role in ['OWNER', 'MANAGER']:
                shops_ids = [x.id for x in shops]
                queryset = queryset.filter(shop_id__in=shops_ids).all()

        category_id = request.query_params.get('category_id')
        if category_id != None:
            history_view_event(obj=category_id,user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            paginated_response = self.get_paginated_response(serializer.data)
            content = paginated_response.data['results']
            del paginated_response.data['results']
            metadata = paginated_response.data
            return Response(custom_api_response(content=content, metadata=metadata), status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED, headers=headers)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfferModel.objects.all()

    serializer_class = OfferSerializer
    # permission_classes = (AllowAny,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        history_view_event(instance,user=request.user)
        count_shown(instance)
        serializer = self.get_serializer(instance)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

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

        #return Response(serializer.data)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)







