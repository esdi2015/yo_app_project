from django.apps import apps
from rest_framework import serializers
from yomarket.models import CardHolder

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


class CardHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardHolder
        fields = ('id','tranzila_tk', 'exp_date')

    def save(self):
        user = self.context['request'].user
        holder=CardHolder(**self.validated_data,user=user)
        holder.save()
        return holder
