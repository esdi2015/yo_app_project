
from rest_framework import serializers
from yomarket.models import WishList,Offer
from api.yomarket.offer.serializers import OfferSerializer
from common.models import User


class WishListSerializator(serializers.ModelSerializer):
    offer = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all())
    def delete(self,user):
        wish = WishList.objects.get(user=user,offer=self.data['offer'])
        wish.delete()

    def create(self, validated_data):
        wish = WishList(**validated_data)
        wish.save()
        return wish


    class Meta:
        model = WishList
        fields=('offer','is_liked')


class WishListNestedSerializator(WishListSerializator):
    is_liked=serializers.HiddenField(default='hide',write_only=True)
    offer = OfferSerializer()