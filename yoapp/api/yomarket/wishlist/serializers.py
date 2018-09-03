
from rest_framework import serializers
from yomarket.models import WishList,Offer
from api.yomarket.offer.serializers import OfferSerializer

class WishListSerializator(serializers.ModelSerializer):
    offer = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all())

    def delete(self,user):
        wish = WishList.objects.get(user=user,offer=self.data['offer'])
        wish.delete()

    class Meta:
        model = WishList
        fields=('offer','is_liked')


class WishListNestedSerializator(WishListSerializator):
    offer = OfferSerializer()