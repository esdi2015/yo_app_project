from django.apps import apps
from rest_framework import serializers
from yomarket.models import CardHolder,Order,OrderProduct,Shop,Coupon,CouponSetting

TransactionModel = apps.get_model('yomarket', 'Transaction')
from api.yomarket.offer.serializers import OfferSerializer,ShopSerializer

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

class CardHolderCreateSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    exp_date = serializers.DateField()


class CheckoutSerializer(serializers.Serializer):
    cart_product_ids = serializers.ListField()
    cardholder_id = serializers.CharField(max_length=20)
    total_sum = serializers.FloatField()
    discount_sum = serializers.FloatField(required=False)
    coupon_id = serializers.CharField(max_length=20,required=False)
    shop_id = serializers.CharField(max_length=20)
    fullname = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=30)


class OrderProductListSerializer(serializers.ModelSerializer):
    offer = OfferSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = ('id', 'offer', 'quantity')


class OrderListSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)
    order_product = OrderProductListSerializer(read_only=True,many=True)
    class Meta:
        model = Order
        fields = ('id', 'created', 'total_sum','status', 'shop','order_product','phone','fullname')


class CouponMakeSerilalizer(serializers.Serializer):
    shop = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all())

class CouponSettingSerilalizer(serializers.ModelSerializer):

    class Meta:
        model = CouponSetting
        fields = ('minimal_price_order',)


class CouponCustomerListSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()
    setting = CouponSettingSerilalizer()
    class Meta:
        model = Coupon
        fields = ('id','discount','discount_type','shop','status','created','setting')