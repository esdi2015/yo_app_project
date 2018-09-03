from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.yomarket.qrcode.serializers import QRcouponSerializator,QRcouponNestedSerializator
from rest_framework import status
from rest_framework import generics

from ...views import custom_api_response

from django.utils import timezone

from yomarket.models import Offer,QRcoupon



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
            return Response(custom_api_response(content={'error':'coupon not exist or invalid'}))
        serializer = self.get_serializer(instance, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.offer.redeemed_codes_increment()
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
            return Response(custom_api_response(content={'error':'coupon not exist or invalid'}))
        serializer = self.get_serializer(instance, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.offer.redeemed_codes_increment()
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)









class QRcouponCheckView(generics.RetrieveAPIView):
    serializer_class = QRcouponNestedSerializator
    model = serializer_class.Meta.model
    lookup_field = 'uuid_id'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.role == 'MANAGER':
            queryset = self.model.objects.filter(offer__shop__manager_id=self.request.user.pk)
        return queryset


class QRcouponShortCheckView(generics.RetrieveAPIView):
    serializer_class = QRcouponNestedSerializator
    model = serializer_class.Meta.model
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.role == 'MANAGER':
            queryset = self.model.objects.filter(offer__shop__manager_id=self.request.user.pk)
        return queryset







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


class QRcouponsListView(generics.ListAPIView):
    serializer_class = QRcouponNestedSerializator
    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        coupons = self.model.objects.filter(user_id=user_id, is_expired=False, is_redeemed=False)
        for coupon in coupons:
            if coupon.expiry_date <= timezone.now():
                coupon.is_expired = True
                coupon.save()
        queryset = self.model.objects.filter(user_id=user_id)
        return queryset

    def list(self,request, *args, **kwargs):
        queryset=self.get_queryset()
        print(queryset)
        if queryset.exists():
            serilizer=self.get_serializer(queryset,many=True)
            return Response(custom_api_response(serilizer),status=status.HTTP_200_OK)
        return Response(custom_api_response(content={'error':'no coupons'}),status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_coupon(request):
    print(request)
    serializer= QRcouponSerializator(data=request.data)
    if serializer.is_valid():
        serializer.save(user_id=request.user.pk)
        return Response(custom_api_response(serializer),status.HTTP_200_OK)
    else:
        return Response(custom_api_response(content={'error':'invalid request data'}),status.HTTP_400_BAD_REQUEST)
