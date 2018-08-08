from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets

from ...views import custom_api_response
from .serializers import ShopSerializer


ShopModel = apps.get_model('yomarket', 'Shop')


class ShopList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        shops = ShopModel.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)



class ShopViewSet(viewsets.ModelViewSet):
    queryset = ShopModel.objects.all()
    serializer_class = ShopSerializer
    permission_classes = (AllowAny,)

    def retrieve(self, request, pk=None):
        queryset = ShopModel.objects.filter(pk=pk).all()
        serializer = ShopSerializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        if (request.user.is_authenticated == True) and (request.user.role == 'OWNER'):
            queryset = ShopModel.objects.filter(user_id=request.user.pk).all()
        else:
            queryset = ShopModel.objects.all()
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #serializer = self.get_serializer(queryset, many=True)
        serializer = ShopSerializer(queryset, many=True)
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
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)