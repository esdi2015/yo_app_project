from django.utils import timezone
from yomarket.models import QRcoupon
from api.yomarket.offer.serializers import OfferSerializer
from rest_framework import serializers
from notification.models import Notification, Subscription
from rest_framework.fields import CurrentUserDefault

from history.utils import history_subscription_event

class NotificationSerializator(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('title', 'body', 'is_data', 'is_sent', 'is_read')



class SubscriptionSerializator(serializers.ModelSerializer):
    category = serializers.StringRelatedField(allow_null=True,required=False)
    category_id = serializers.IntegerField(allow_null=True,required=False)
    shop = serializers.StringRelatedField(allow_null=True,required=False)
    shop_id = serializers.IntegerField(allow_null=True,required=False)

    def create(self, validated_data):
        try:
            sub,created=Subscription.objects.update_or_create(user=self.context['request'].user,shop_id=validated_data['shop_id'],type=validated_data['type'],defaults={**validated_data})
            history_subscription_event(obj=sub.shop,user=self.context['request'].user)
        except KeyError:
            sub,created=Subscription.objects.update_or_create(user=self.context['request'].user,category_id=validated_data['category_id'],type=validated_data['type'],defaults={**validated_data})
            history_subscription_event(obj=sub.category,user=self.context['request'].user)
        return sub

    class Meta:
        model = Subscription
        fields=('id', 'type', 'category', 'category_id', 'shop','shop_id', 'discount_filter', 'discount_value', 'notification_type')