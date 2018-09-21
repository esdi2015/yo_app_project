from django.apps import apps
from rest_framework import serializers


TransactionModel = apps.get_model('yomarket', 'Transaction')
from api.yomarket.offer.serializers import OfferSerializer

class TransactionSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    customer_id = serializers.IntegerField(allow_null=False)
    manager = serializers.StringRelatedField()
    manager_id = serializers.IntegerField(allow_null=False)
    offer = serializers.StringRelatedField()
    offer_id = serializers.IntegerField(allow_null=False)
    points = serializers.IntegerField(allow_null=False, default=0, required=False)


    class Meta:
        model = TransactionModel
        fields = ('id', 'customer', 'customer_id', 'manager', 'manager_id',
                  'offer', 'offer_id', 'points', 'created')



class MyTransactionSerializer(TransactionSerializer):

    offer = OfferSerializer( read_only=True)

