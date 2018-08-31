from yomarket.models import QRcoupon,Offer
from rest_framework import serializers
from django.utils import timezone
from common.models import User
from yomarket.models import QRcoupon

from api.yomarket.offer.serializers import OfferSerializer

class QRcouponSerializator(serializers.ModelSerializer):
    offer = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all())
    expiry_date = serializers.DateTimeField(required=False)

    def create(self,validated_data):
          offer = validated_data['offer']
          user_id = validated_data['user_id']

          try:
            coupon = QRcoupon.objects.get(offer=offer,user_id=user_id,type=offer.code_type)
          except QRcoupon.DoesNotExist:
            coupon = QRcoupon(**validated_data,expiry_date=offer.expire,type=offer.code_type)
            coupon.save()

          return coupon

    class Meta:
        model = QRcoupon
        fields = ('uuid_id','id','offer','is_redeemed','expiry_date','is_expired','type')



class QRcouponNestedSerializator(QRcouponSerializator):
    offer = OfferSerializer()