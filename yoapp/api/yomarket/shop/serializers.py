from django.apps import apps
from rest_framework import serializers
from ...common.category.serializers import CategorySerializer
from ..schedule.serializers import ScheduleSerializer
from notification.models import Subscription

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
    is_subscribed = serializers.SerializerMethodField()
    schedule = ScheduleSerializer(many=False, read_only=True)


    def get_is_subscribed (self, obj):
        try:
            wish = Subscription.objects.get(user_id=self.context['request'].user.id, shop=obj)
            return True
        except Subscription.DoesNotExist:
            return False


    class Meta:
        model = ShopModel
        fields = ('id', 'title', 'address', 'description', 'user', 'user_id', 'manager', 'manager_id',
                  'latitude', 'longitude', 'outer_link', 'social_link', 'phone', 'image', 'code_type', 'city', 'city_id',
                  'categories','is_subscribed', 'schedule')


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
    is_open = serializers.SerializerMethodField()

    def get_is_open(self, obj):
        return True

    class Meta:
        model = ShopModel
        fields = ('id', 'title', 'address', 'description', 'user', 'user_id', 'manager', 'manager_id',
                  'outer_link', 'social_link', 'phone', 'image', 'code_type', 'city', 'city_id', 'categories',
                  'is_subscribed', 'is_open')