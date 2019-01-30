from django.apps import apps
from rest_framework import serializers
from ..shop.serializers import ShopSerializer
from yomarket.models import WishList, SecondaryInfo,QRcoupon,CartProduct,Coupon,CouponSetting
import datetime
from django.utils import timezone


OfferModel = apps.get_model('yomarket', 'Offer')



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
    can_get_coupons = serializers.SerializerMethodField()


    def get_can_get_coupons(self,obj):
        if self.context['request'].user.is_authenticated == True:
            settings = CouponSetting.objects.filter(rank__lte=self.context['request'].user.profile.rank, shop=obj.shop)
            can_get = False
            for setting in settings:
                coupons_count = Coupon.objects.filter(setting=setting).count()
                if coupons_count < setting.coupons_per_user:
                    can_get = True
        else:
            can_get = False
        return can_get

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
                  'is_expired', 'is_visible', 'status','can_get_coupons')

    def validate_catedory_id(value):
        if value.isnumeric() == False:
            raise serializers.ValidationError('must be numeric.')





class CartProductListSerializer(serializers.ModelSerializer):
    offer = OfferSerializer(read_only=True)
    class Meta:
        model = CartProduct
        fields = ('id','offer','quantity')

class CartProductDeleteSerializer(serializers.ModelSerializer):
    id = serializers.ListField()
    class Meta:
        model = CartProduct
        fields = ('id',)


class CartProductCreateSerializer(CartProductListSerializer):
    offer = serializers.PrimaryKeyRelatedField(queryset=OfferModel.objects.all())

    def create(self, validated_data):
        cart_product=CartProduct(user=self.context['request'].user,**validated_data)
        cart_product.save()
        return cart_product

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    class Meta:
        model = CartProduct
        fields = ('offer','quantity')