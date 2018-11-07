from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.yomarket.qrcode.serializers import QRcouponSerializator, QRcouponNestedSerializator
from rest_framework import status
from rest_framework import generics
from api.views import CustomPagination, prepare_paginated_response
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, BooleanFilter, CharFilter
from rest_framework import filters

from ...views import custom_api_response

from django.utils import timezone
from yomarket.models import Offer, QRcoupon
from statistic.utlis import count_taken_coupons, count_redeemd_coupons
from ...utils import ERROR_API
from history.utils import history_make_coupon_event,history_redeem_coupon_event
from yomarket.models import Transaction
from django.core.exceptions import ValidationError

class QRcouponRedeemView(generics.UpdateAPIView):
    serializer_class = QRcouponSerializator
    lookup_field = 'uuid_id'
    permission_classes = (IsAuthenticated,)


    def get_object(self):
        if self.request.user.role == 'MANAGER':
            try:
                obj = QRcoupon.objects.get(offer__shop__manager_id=self.request.user.pk,is_redeemed=False,uuid_id=self.kwargs.get('uuid_id'))
                return obj
            except QRcoupon.DoesNotExist:
                return None



    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance == None:
            error = {"detail": ERROR_API['208'][1]}
            error_codes = [ERROR_API['208'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        trans = Transaction(customer=instance.user, manager=request.user, points=1, offer=instance.offer)
        trans.save()
        instance.offer.redeemed_codes_increment()
        count_redeemd_coupons(instance.offer)
        history_redeem_coupon_event(obj=instance.offer,user=request.user)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)




class QRcouponShortRedeemView(generics.UpdateAPIView):
    serializer_class = QRcouponSerializator
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)


    def get_object(self):
        if self.request.user.role == 'MANAGER':
            try:
                obj = QRcoupon.objects.get(offer__shop__manager_id=self.request.user.pk,is_redeemed=False,id=self.kwargs.get('id'))
                return obj
            except QRcoupon.DoesNotExist:
                return None



    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == None:
            error = {"detail": ERROR_API['208'][1]}
            error_codes = [ERROR_API['208'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        trans = Transaction(customer=instance.user, manager=request.user, points=1, offer=instance.offer)
        trans.save()
        count_redeemd_coupons(instance.offer)
        instance.offer.redeemed_codes_increment(user=self.request.user)
        history_redeem_coupon_event(obj=instance.offer,user=request.user)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)




class QRcouponCheckView(generics.RetrieveAPIView):
    serializer_class = QRcouponNestedSerializator
    model = serializer_class.Meta.model
    lookup_field = 'uuid_id'
    permission_classes = (IsAuthenticated,)


    def get_object(self):
        if self.request.user.role == 'MANAGER':
            try:
                obj = QRcoupon.objects.get(offer__shop__manager_id=self.request.user.pk,uuid_id=self.kwargs.get('uuid_id'))
                return obj
            except (QRcoupon.DoesNotExist, ValidationError) as err:
                return None


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == None:
            error = {"detail": ERROR_API['208'][1]}
            error_codes = [ERROR_API['208'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


class QRcouponShortCheckView(generics.RetrieveAPIView):
    serializer_class = QRcouponNestedSerializator
    model = serializer_class.Meta.model
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)



    def get_object(self):
        if self.request.user.role == 'MANAGER':
            try:
                obj = QRcoupon.objects.get(offer__shop__manager_id=self.request.user.pk,id=self.kwargs.get('id'))
                return obj
            except (QRcoupon.DoesNotExist, ValidationError) as err:
                return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == None:
            error = {"detail": ERROR_API['208'][1]}
            error_codes = [ERROR_API['208'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)






#
# class QRcouponsListView(generics.ListAPIView):
#     serializer_class = QRcouponSerializator
#     model = serializer_class.Meta.model
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         user_id = self.request.user.pk
#         coupons = self.model.objects.filter(user_id=user_id,is_expired=False, is_redeemed=False)
#         for coupon in coupons:
#             if coupon.expiry_date <= timezone.now():
#                 coupon.is_expired=True
#                 coupon.save()
#         if self.request.query_params.get('type') =='expired':
#             queryset = self.model.objects.filter(user_id=user_id, is_expired=True)
#         elif self.request.query_params.get('type') =='redeemed':
#             queryset = self.model.objects.filter(user_id=user_id, is_redeemed=True)
#         else:
#             queryset = self.model.objects.filter(user_id=user_id, is_expired=False, is_redeemed=False)
#         return queryset
#
#
#




class QRcouponListFilter(FilterSet):
    category_ids = CharFilter(method='filter_category_ids')
    category_id = CharFilter(method='filter_category_id')

    shop_ids = CharFilter(method='filter_shop_ids')
    shop_id = CharFilter(method='filter_shop_ids')


    class Meta:
        model = QRcoupon
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




class QRcouponsListView(generics.ListAPIView):
    serializer_class = QRcouponNestedSerializator
    filter_class = QRcouponListFilter
    pagination_class = CustomPagination

    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        coupons = self.model.objects.filter(user_id=user_id, is_expired=False, is_redeemed=False)
        for coupon in coupons:
            if coupon.expiry_date <= timezone.now():
                coupon.is_expired = True
                coupon.delete()
        queryset = self.model.objects.filter(user_id=user_id)
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
@permission_classes([IsAuthenticated])
def make_coupon(request):
    print(request)
    serializer= QRcouponSerializator(data=request.data)
    if serializer.is_valid():
        instance=serializer.save(user_id=request.user.pk)
        count_taken_coupons(instance.offer)
        history_make_coupon_event(obj=instance.offer,user=request.user)
        serializer=QRcouponNestedSerializator(instance,context={'request': request})
        return Response(custom_api_response(serializer),status.HTTP_200_OK)
    else:
        return Response(custom_api_response(content={'error':'invalid request data'}),status.HTTP_400_BAD_REQUEST)
