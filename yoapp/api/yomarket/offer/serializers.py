from django.apps import apps
from rest_framework import serializers
from ..shop.serializers import ShopSerializer
from yomarket.models import WishList, SecondaryInfo,QRcoupon
import datetime
from django.utils import timezone


OfferModel = apps.get_model('yomarket', 'Offer')

class CartAddSerializer(serializers.Serializer):
    offers_ids = serializers.ListField()


class SecondaryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SecondaryInfo
        fields = ('id','title','text')



class OfferSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()
    shop_id = serializers.IntegerField(allow_null=False)
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField(allow_null=True)
    is_liked = serializers.SerializerMethodField()
    secondary_info = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    is_visible = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        try:
            wish= WishList.objects.get(user_id=self.context['request'].user.id,offer=obj)
            return True
        except WishList.DoesNotExist:
            return False

    def get_secondary_info (self, obj):
            info = SecondaryInfo.objects.filter(offer=obj)
            serializer=SecondaryInfoSerializer(info,many=True)
            return serializer.data

    def get_is_expired(self, obj):
        now_datetime = timezone.now()
        expire_datetime = obj.expire
        if expire_datetime >= now_datetime:
            return False
        else:
            return True

    def get_is_visible(self, obj):
        try:
            coupon = QRcoupon.objects.get(is_redeemed=False,is_expired=False,user_id=self.context['request'].user.id, offer=obj)
            return False
        except QRcoupon.DoesNotExist:
            return True

    class Meta:
        model = OfferModel
        fields = ('id', 'category', 'category_id', 'shop', 'shop_id', 'title', 'image', 'short_description',
                  'description', 'price', 'discount', 'discount_type', 'code_data', 'created', 'code_type',
                  'offer_type', 'expire','is_liked','secondary_info','redeemed_codes_count','codes_count',
                  'is_expired', 'is_visible', 'status')

    def validate_catedory_id(value):
        if value.isnumeric() == False:
            raise serializers.ValidationError('must be numeric.')
