
from django.apps import apps
from rest_framework import serializers
from ..shop.serializers import ShopSerializer
from yomarket.models import WishList
OfferModel = apps.get_model('yomarket', 'Offer')


class OfferSerializer(serializers.ModelSerializer): #serializers.HyperlinkedModelSerializer #ModelSerializer
    shop = serializers.StringRelatedField()
    #shop = serializers.SlugRelatedField(slug_field='title', read_only=True, many=False)
    #shop = ShopSerializer(source='shop_offer')
    #shop = ShopSerializer(source='title')
    shop_id = serializers.IntegerField(allow_null=False)
    category = serializers.StringRelatedField()  #source='category.category_name'
    category_id = serializers.IntegerField(allow_null=True)
    #code_type = serializers.StringRelatedField()
    #code_type = serializers.HyperlinkedRelatedField()
    is_liked = serializers.SerializerMethodField()
    def get_is_liked(self, obj):
        try:
            wish= WishList.objects.get(user_id=self.context['request'].user.id,offer=obj)
            return True
        except WishList.DoesNotExist:
            return False


    class Meta:
        model = OfferModel
        fields = ('id', 'category', 'category_id', 'shop', 'shop_id', 'title', 'image', 'short_description',
                  'description', 'price', 'discount', 'discount_type', 'code_data', 'created', 'code_type',
                  'offer_type', 'expire','is_liked')
        #depth = 3
        #order_by = (('shop',))


    def validate_catedory_id(value):
        if value.isnumeric() == False:
            raise serializers.ValidationError('must be numeric.')

    # def get_category(self, obj):
    #     return obj.category.category_name


    # def get_shop(self, obj):
    #     return obj.shop.title