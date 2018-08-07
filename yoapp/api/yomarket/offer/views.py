from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ...views import custom_api_response
from .serializers import OfferSerializer

from rest_framework.pagination import LimitOffsetPagination


OfferModel = apps.get_model('yomarket', 'Offer')


class OfferList(APIView):  #, LimitOffsetPagination
    permission_classes = (AllowAny,)
    #ordering_fields = ('title', 'price')

    def get(self, request, format=None, pk=None):
        offers = OfferModel.objects.all() # .filter(category_id=2)

        if pk is not None:
            #offers = get_object_or_404(offers, pk=pk)
            offers = OfferModel.objects.filter(pk=pk).all()
            serializer = OfferSerializer(offers, many=True)
        else:
            category_id = self.request.query_params.get('category_id', None)
            if category_id is not None:
                #from .serializers import catedory_id_validate
                #catedory_id_validate(category_id)
                offers = offers.filter(category_id=category_id)

            shop_id = self.request.query_params.get('shop_id', None)
            if shop_id is not None:
                offers = offers.filter(shop_id=shop_id)

            ordering = self.request.query_params.get('ordering', None)
            if ordering is not None:
                ordering = ordering.split(',')
                offers = offers.order_by(*ordering)

            # page = self.paginate_queryset(offers)
            # if page is not None:
            #     serializer = self.get_serializer(page, many=True)
            #     return self.get_paginated_response(serializer.data)

            serializer = OfferSerializer(offers, many=True)

        response = Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        return response


    def post(self, request, format=None):
        #usernames = [user.username for user in User.objects.all()]
        #return Response(usernames)
        pass



class OfferSearchView(generics.ListAPIView):
    queryset = OfferModel.objects.all()

    serializer_class = OfferSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description',)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            content = paginated_response.data['results']
            del paginated_response.data['results']
            metadata = paginated_response.data
            return Response(custom_api_response(content=content, metadata=metadata), status=status.HTTP_200_OK)


        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
