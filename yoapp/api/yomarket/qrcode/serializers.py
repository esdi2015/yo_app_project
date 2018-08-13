from django.utils import timezone
import uuid
from yomarket.models import QRcoupon
from api.yomarket.offer.serializers import OfferSerializer
from rest_framework import serializers


class QRcouponSerializator(serializers.ModelSerializer):
    offer = OfferSerializer()

    def validate_expiry_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Coupon is expiried.")
        return value

    def validate_available(self, attrs):
        pass

    def create(self, user, offer):
        qrcoupon = self.Meta.model(expiry_date=timezone.now(),offer=offer)
        qrcoupon.save()
        return qrcoupon


    class Meta:
        model = QRcoupon
        fields = ('uuid_id', 'offer')