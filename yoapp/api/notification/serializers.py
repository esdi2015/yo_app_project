from django.utils import timezone
from yomarket.models import QRcoupon
from api.yomarket.offer.serializers import OfferSerializer
from rest_framework import serializers
from notification.models import Notification, Subscription


class NotificationSerializator(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('title', 'body', 'is_data', 'is_sent', 'is_read')



class SubscriptionSerializator(serializers.ModelSerializer):
    category = serializers.StringRelatedField(allow_null=True,required=False)
    category_id = serializers.IntegerField(allow_null=True,required=False)
    shop = serializers.StringRelatedField(allow_null=True,required=False)
    shop_id = serializers.IntegerField(allow_null=True,required=False)

    class Meta:
        model = Subscription
        fields=('id', 'type', 'category', 'category_id', 'shop','shop_id', 'discount_filter', 'discount_value', 'notification_type')