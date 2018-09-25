from django.apps import apps
from rest_framework import serializers
from ...common.category.serializers import CategorySerializer
from ..schedule.serializers import ScheduleSerializer
from notification.models import Subscription
import datetime


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
    schedule_id = serializers.IntegerField(allow_null=True, required=False)


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
                  'categories','is_subscribed', 'schedule', 'schedule_id', 'logo')


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


def get_now_day():
    return datetime.datetime.now().strftime("%a").lower()



class ShopListSerializer(ShopSerializer):
    is_open = serializers.SerializerMethodField()
    schedule_title = serializers.StringRelatedField(source='schedule.title')

    def get_is_open(self, obj):
        now_time = datetime.datetime.now().time()
        now_day = get_now_day()
        open = now_day + "_open"
        close = now_day + "_close"

        if obj.schedule:
            open_time = getattr(obj.schedule, open, None)
            close_time = getattr(obj.schedule, close, None)
            if open_time and close_time:
                if (open_time < now_time) and (close_time > now_time):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return None


    class Meta:
        model = ShopModel
        fields = ('id', 'title', 'address', 'description', 'user', 'user_id', 'manager', 'manager_id',
                  'outer_link', 'social_link', 'phone', 'image', 'code_type', 'city', 'city_id', 'categories',
                  'is_subscribed', 'is_open', 'schedule_id', 'schedule_title', 'logo')