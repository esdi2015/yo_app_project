from django.utils import timezone
from yomarket.models import QRcoupon
from api.yomarket.offer.serializers import OfferSerializer
from rest_framework import serializers
from notification.models import Notification, Subscription

class NotificationSerializator(serializers.ModelSerializer):


    class Meta:
        model = Notification
        fields = ('title', 'body','is_data')

class SubscriptionSerializator(serializers.ModelSerializer):


    class Meta:
        model = Subscription
        fields=('type','category','shop','discount_filter','discount_value')