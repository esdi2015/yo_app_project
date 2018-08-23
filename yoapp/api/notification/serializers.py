from django.utils import timezone
from yomarket.models import QRcoupon
from api.yomarket.offer.serializers import OfferSerializer
from rest_framework import serializers
from notification.models import Notification, Subscription


class NotificationSerializator(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('title', 'body', 'is_data')



class SubscriptionSerializator(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField(allow_null=False)

    class Meta:
        model = Subscription
        fields=('id', 'type', 'category', 'category_id', 'shop', 'discount_filter', 'discount_value')