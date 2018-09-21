from django.apps import apps
from rest_framework import serializers


ScheduleModel = apps.get_model('yomarket', 'Schedule')


class ScheduleSerializer(serializers.ModelSerializer):
    mon_open = serializers.TimeField(format='%H:%M', allow_null=True)  #input_formats='%I:%M %p'
    mon_close = serializers.TimeField(format='%H:%M', allow_null=True)
    tue_open = serializers.TimeField(format='%H:%M', allow_null=True)
    tue_close = serializers.TimeField(format='%H:%M', allow_null=True)
    wed_open = serializers.TimeField(format='%H:%M', allow_null=True)
    wed_close = serializers.TimeField(format='%H:%M', allow_null=True)
    thu_open = serializers.TimeField(format='%H:%M', allow_null=True)
    thu_close = serializers.TimeField(format='%H:%M', allow_null=True)
    fri_open = serializers.TimeField(format='%H:%M', allow_null=True)
    fri_close = serializers.TimeField(format='%H:%M', allow_null=True)
    sat_open = serializers.TimeField(format='%H:%M', allow_null=True)
    sat_close = serializers.TimeField(format='%H:%M', allow_null=True)
    sun_open = serializers.TimeField(format='%H:%M', allow_null=True)
    sun_close = serializers.TimeField(format='%H:%M', allow_null=True)
    shop = serializers.StringRelatedField()
    shop_id = serializers.IntegerField(allow_null=False)

    class Meta:
        model = ScheduleModel
        fields = ('id', 'title', 'shop', 'shop_id', 'mon_open', 'mon_close', 'tue_open', 'tue_close',
                  'wed_open', 'wed_close', 'thu_open', 'thu_close', 'fri_open', 'fri_close',
                  'sat_open', 'sat_close', 'sun_open', 'sun_close')
