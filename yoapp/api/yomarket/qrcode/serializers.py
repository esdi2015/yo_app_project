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

          def make_coupon():
              coupon = QRcoupon(**validated_data, expiry_date=timezone.now()+timezone.timedelta(seconds=900), type=offer.code_type,
                                alpha_num_code_type=offer.alpha_num_code_type,
                                coupon_phone=offer.coupon_phone,
                                coupon_web=offer.coupon_web,
                                description=offer.coupon_description)
              return coupon

          try:
            coupon = QRcoupon.objects.get(offer=offer,user_id=user_id,type=offer.code_type,
                                          alpha_num_code_type=offer.alpha_num_code_type,
                                          coupon_phone=offer.coupon_phone,
                                          coupon_web=offer.coupon_web,
                                          description=offer.coupon_description
                                          )
            if coupon.expiry_date <= timezone.now():
               coupon.is_expired = True
               coupon.delete()
               coupon=make_coupon()
               coupon.save()
          except QRcoupon.DoesNotExist:
            coupon=make_coupon()
            coupon.save()
            if coupon.expiry_date <= timezone.now():
               coupon.is_expired = True
               coupon.delete()

          return coupon

    class Meta:
        model = QRcoupon
        fields = ('uuid_id','id','offer','is_redeemed','expiry_date','is_expired','type','alpha_num_code_type','coupon_phone','coupon_web','description')



class QRcouponNestedSerializator(QRcouponSerializator):
    offer = OfferSerializer()