from django.apps import apps
from rest_framework import serializers
from ..shop.serializers import ShopSerializer


OfferModel = apps.get_model('yomarket', 'Offer')


class OfferSerializer(serializers.ModelSerializer): #serializers.HyperlinkedModelSerializer #ModelSerializer
    shop = serializers.StringRelatedField()
    #shop = ShopSerializer(source='shop_offer')
    shop_id = serializers.IntegerField(allow_null=False)
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField(allow_null=True)
    #code_type = serializers.StringRelatedField()
    #code_type = serializers.HyperlinkedRelatedField()


    class Meta:
        model = OfferModel
        fields = ('id', 'category', 'category_id', 'shop', 'shop_id', 'title', 'image', 'short_description',
                  'description', 'price', 'discount', 'discount_type', 'code_data', 'created', 'code_type',
                  'offer_type', 'expire')
        #depth = 2


    def validate_catedory_id(value):
        if value.isnumeric() == False:
            raise serializers.ValidationError('must be numeric.')