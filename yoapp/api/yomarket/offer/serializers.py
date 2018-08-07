from django.apps import apps
from rest_framework import serializers


OfferModel = apps.get_model('yomarket', 'Offer')


class OfferSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()
    shop_id = serializers.IntegerField(allow_null=False)
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField(allow_null=True)


    class Meta:
        model = OfferModel
        fields = ('id', 'category', 'category_id', 'shop', 'shop_id', 'title', 'image', 'short_description',
                  'description', 'price', 'discount', 'discount_type', 'code_data', 'created')


    def validate_catedory_id(value):
        if value.isnumeric() == False:
            raise serializers.ValidationError('must be numeric.')