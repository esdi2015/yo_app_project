import datetime
import traceback
from django.apps import apps
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.utils import model_meta
from ...common.category.serializers import CategorySerializer
from ..schedule.serializers import ScheduleSerializer
from notification.models import Subscription
from api.serializers import MultipartM2MField


ShopModel = apps.get_model('yomarket', 'Shop')
Category = apps.get_model('common', 'Category')


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
    is_subscribed = serializers.SerializerMethodField()
    schedule = ScheduleSerializer(many=False, read_only=True)
    schedule_id = serializers.IntegerField(allow_null=True, required=False)

    def get_is_subscribed (self, obj):
            wish = Subscription.objects.filter(user_id=self.context['request'].user.id, shop=obj)
            if wish.exists():
                return True
            else:
                return False
    class Meta:
        model = ShopModel
        fields = ('id', 'title', 'address', 'description', 'user', 'user_id', 'manager', 'manager_id',
                  'latitude', 'longitude', 'outer_link', 'social_link', 'phone', 'image', 'code_type', 'city', 'city_id',
                  'categories','is_subscribed', 'schedule', 'schedule_id', 'logo')



class ShopCreateUpdateSerializer(ShopSerializer):
    categories = MultipartM2MField(allow_null=True, required=False)

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                if attr == 'categories':
                    if value is None:
                        instance.categories.clear()
                    else:
                        try:
                            categories_data = Category.objects.filter(id__in=value).all()
                            field = getattr(instance, attr)
                            field.set(value)
                        except IntegrityError as e:
                            pass
                else:
                    field = getattr(instance, attr)
                    field.set(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance


    def to_representation(self, instance):
        representation = super(ShopCreateUpdateSerializer, self).to_representation(instance)
        categories = Category.objects.filter(id__in=representation['categories']).all()
        categories_serializer = CategorySerializer(categories, many=True)
        representation['categories'] = categories_serializer.data
        return representation




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
                  'latitude', 'longitude','outer_link', 'social_link', 'phone', 'image', 'code_type', 'city', 'city_id', 'categories',
                  'is_subscribed', 'is_open', 'schedule_id', 'schedule_title', 'logo')