from rest_framework import serializers
from api.yomarket.transaction.serializers import TransactionSerializer


class OfferSerializer(serializers.Serializer):
    offer__title  = serializers.CharField()
    views = serializers.IntegerField()

class ShopSerializer(serializers.Serializer):
    shop_name = serializers.CharField()
    views = serializers.IntegerField()


class ManagerSerializer(serializers.Serializer):
    manager__email = serializers.CharField()

class OverviewOwnerSerializer(serializers.Serializer):
        offers =  OfferSerializer(many=True,allow_null=True)
        shops = ShopSerializer(many=True,allow_null=True)
        transactions = TransactionSerializer(many=True)
        managers = ManagerSerializer(many=True,allow_null=True)


class OverviewManagerSerializer(serializers.Serializer):
    offers = OfferSerializer(many=True, allow_null=True)
    transactions = TransactionSerializer(many=True)
