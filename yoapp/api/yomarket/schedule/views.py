from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import filters
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from ...views import custom_api_response
from .serializers import ScheduleSerializer


ScheduleModel = apps.get_model('yomarket', 'Schedule')

#OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')
UserModel = get_user_model()


class ScheduleListView(generics.ListCreateAPIView):
    queryset = ScheduleModel.objects.all()

    serializer_class = ScheduleSerializer
    #permission_classes = (AllowAny,)
    #filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    #search_fields = ('description', 'title')
    filter_fields = ('shop_id', )
    #ordering_fields = '__all__'
    #ordering_fields = ('shop')
    # ordering_fields = ('shop__title', 'category__category_name', 'title', 'image',
    #                    'short_description', 'price', 'offer_type', 'expire', )


    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.user.is_authenticated == True:
            if request.user.role == 'OWNER':
                shops = ShopModel.objects.filter(user_id=request.user.pk).all()
            elif request.user.role == 'MANAGER':
                shops = ShopModel.objects.filter(manager_id=request.user.pk).all()

            if request.user.role in ['OWNER', 'MANAGER']:
                shops_ids = [x.id for x in shops]
                queryset = queryset.filter(shop_id__in=shops_ids).all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True,context={'request': request})
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


class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ScheduleModel.objects.all()

    serializer_class = ScheduleSerializer
    # permission_classes = (AllowAny,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
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








# class ScheduleViewSet(viewsets.ModelViewSet):
#     queryset = ScheduleModel.objects.all()
#     serializer_class = ScheduleSerializer
#     #permission_classes = (AllowAny,)
#
#     #filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
#     #search_fields = ('title', 'address', )
#     #filter_fields = ('manager_id', )
#     #ordering_fields = '__all__'
#
#     def get_permissions(self):
#         if self.action == 'retrieve' or self.action == 'list':
#             return [AllowAny(), ]  # AllowAny(), - remove it later, need to add  IsAuthenticated() !!!
#         else :
#             return []
#
#     def retrieve(self, request, pk=None):
#         queryset = ScheduleModel.objects.filter(pk=pk).all()
#         serializer = ScheduleSerializer(queryset, many=True)
#         return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
#
#
#     def list(self, request, *args, **kwargs):
#
#         # if (request.user.is_authenticated == True) and (request.user.role == 'OWNER'):
#         #     queryset = ShopModel.objects.filter(user_id=request.user.pk).all()
#         # else:
#         #     queryset = ShopModel.objects.all()
#
#         #queryset = self.filter_queryset(self.queryset)
#         queryset = ScheduleModel.objects.all()
#
#         # page = self.paginate_queryset(queryset)
#         # if page is not None:
#         #     serializer = self.get_serializer(page, many=True)
#         #     return self.get_paginated_response(serializer.data)
#         #serializer = self.get_serializer(queryset, many=True)
#         serializer = ScheduleSerializer(queryset, many=True)
#         return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
    #
    #
    # def create(self, request, *args, **kwargs):
    #     request.data['user_id'] = request.user.pk
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED, headers=headers)
    #
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     request.data['user_id'] = request.user.pk
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(custom_api_response(serializer), status=status.HTTP_200_OK)