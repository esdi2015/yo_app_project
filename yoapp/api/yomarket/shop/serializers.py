from django.apps import apps
from rest_framework import serializers
from ...common.category.serializers import CategorySerializer


ShopModel = apps.get_model('yomarket', 'Shop')


class ShopSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(allow_null=True, required=False)
    manager = serializers.StringRelatedField()
    manager_id = serializers.IntegerField(allow_null=True, required=False)
    latitude = serializers.FloatField(allow_null=True, required=False)
    longitude = serializers.FloatField(allow_null=True, required=False)
    outer_link = serializers.CharField(allow_null=True, required=False)
    phone = serializers.CharField(allow_null=True, required=False)
    city = serializers.StringRelatedField()
    city_id = serializers.IntegerField(allow_null=True, required=False)
    categories = CategorySerializer(many=True, read_only=True)
    #image = serializers.ImageField(upload_to='shops/%Y/%m/%d', blank=True)

    class Meta:
        model = ShopModel
        fields = ('id', 'title', 'address', 'description', 'user', 'user_id', 'manager', 'manager_id',
                  'latitude', 'longitude', 'outer_link', 'social_link', 'phone', 'image', 'code_type', 'city', 'city_id',
                  'categories')


    # def save(self, **kwargs):
    #     super().save(self, **kwargs)

    # def to_representation(self, instance):
    #     # instance is the model object. create the custom json format by accessing instance attributes normaly
    #     # and return it
    #     identifiers = dict()
    #     identifiers['id'] = instance.id
    #     identifiers['title'] = instance.title
    #
    #     representation = {
    #         'identifiers': identifiers,
    #         #'user_id': instance.user_id,
    #         'address': instance.address
    #     }
    #
    #     return representation


class ShopListSerializer(ShopSerializer):

    class Meta:
        model = ShopModel
        fields = ('id', 'title', 'address', 'description', 'user', 'user_id', 'manager', 'manager_id',
                  'outer_link', 'social_link', 'phone', 'image', 'code_type', 'city', 'city_id', 'categories')