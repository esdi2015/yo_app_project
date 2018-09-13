from django.utils import timezone
from rest_framework import serializers

from statistic.models import StatisticTable
from yomarket.models import Offer

class StatisticTableSerializer(serializers.ModelSerializer):
    offer = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all())
    class Meta:
        model = StatisticTable
        fields = ('offer','shop','type')


class OfferTakenRedeemedSerializer(serializers.Serializer):
    date_field = serializers.DateTimeField(allow_null=True,required=False)
    taken = serializers.IntegerField(allow_null=True)
    redeemed = serializers.IntegerField(allow_null=True)

class OfferLikedViewsSerializer(serializers.Serializer):
    date_field = serializers.DateTimeField(allow_null=True,required=False)
    liked = serializers.IntegerField(allow_null=True)
    shown = serializers.IntegerField(allow_null=True)


class CategoryPieSerializer(serializers.Serializer):
    category_name=serializers.CharField()
    total = serializers.IntegerField()


class ShopPieSerializer(serializers.Serializer):
    shop_name=serializers.CharField()
    total = serializers.IntegerField()


class OfferPieSerializer(serializers.Serializer):
    offer_name=serializers.CharField()
    total = serializers.IntegerField()