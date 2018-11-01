from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, BooleanFilter, CharFilter

from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters


from api.views import custom_api_response

from yomarket.models import WishList
from .serializers import WishListSerializator,WishListNestedSerializator
from statistic.utlis import count_liked

UserModel=get_user_model()
from api.views import CustomPagination, prepare_paginated_response


from django.apps import apps
from rest_framework import generics
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError
from ...utils import ERROR_API
from history.utils import history_like_event


class WishListListFilter(FilterSet):
    category_ids = CharFilter(method='filter_category_ids')
    category_id = CharFilter(method='filter_category_id')

    shop_ids = CharFilter(method='filter_shop_ids')
    shop_id = CharFilter(method='filter_shop_ids')


    class Meta:
        model = WishList
        fields = ('category_id', 'offer__shop_id',
                  'category_ids', 'shop_ids')



    def filter_category_ids(self, queryset, name, value):
        if value:
            queryset = queryset.filter(offer__category_id__in=value.strip().split(',')).all()
        return queryset

    def filter_category_id(self, queryset, name, value):
        if value:
            queryset = queryset.filter(offer__category_id=value).all()
        return queryset


    def filter_shop_ids(self, queryset, name, value):
        if value:
            queryset = queryset.filter(offer__shop_id__in=value.strip().split(',')).all()
        return queryset

    def filter_shop_id(self, queryset, name, value):
        if value:
            queryset = queryset.filter(offer__shop_id_=value).all()
        return queryset





class MyCouponsListView(generics.ListAPIView):
    serializer_class = WishListNestedSerializator
    filter_class = WishListListFilter
    pagination_class = CustomPagination
    model = WishList

    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)

    def get_queryset(self):
        user_id = self.request.user.pk
        queryset = self.model.objects.filter(user_id=user_id,offer__expire__gte=timezone.now())
        return queryset

    def list(self,request, *args, **kwargs):
        queryset=self.filter_queryset(self.get_queryset())
        if queryset.exists():

            paginate = prepare_paginated_response(self, request, queryset)
            if paginate:
                return Response(custom_api_response(content=paginate.content, metadata=paginate.metadata),
                                status=status.HTTP_200_OK)

            serilizer=self.get_serializer(queryset,many=True)
            return Response(custom_api_response(serilizer),status=status.HTTP_200_OK)

        error = {"detail": ERROR_API['200'][1]}
        error_codes = [ERROR_API['200'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes(())
def unlike(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    serializer = WishListSerializator(data=request.data)

    if serializer.is_valid():
        try:
             serializer.delete(user=request.user)
        except WishList.DoesNotExist:
            return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(())
def like(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    serializer = WishListSerializator(data=request.data)

    if serializer.is_valid():
        instance=serializer.save(user=request.user)
        history_like_event(obj=instance.offer,user=request.user)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)



class LikeView(generics.CreateAPIView):
    serializer_class = WishListSerializator
    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated,)


    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            instance=serializer.save(user=self.request.user)
            count_liked(instance.offer)
            history_like_event(obj=instance.offer,user=request.user)
            return Response(custom_api_response(serializer), status.HTTP_200_OK)
        except IntegrityError:
            return Response(custom_api_response(content={'is_liked':True}),status.HTTP_200_OK)





@api_view(['GET'])
@permission_classes(())
def is_liked(request,offer_id):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    try:
        wishlist= WishList.objects.get(user=request.user,offer=offer_id)
    except WishList.DoesNotExist:
        return Response(custom_api_response(content={'offer':int(offer_id),'is_liked':False}),status.HTTP_200_OK)
    serializer=WishListSerializator(wishlist)
    return Response (custom_api_response(serializer),status.HTTP_200_OK)

