from django.apps import apps
from rest_framework import serializers


ScheduleModel = apps.get_model('yomarket', 'Schedule')


class ScheduleSerializer(serializers.ModelSerializer):
    mon_open = serializers.TimeField(format='%H:%M', )  #input_formats='%I:%M %p'
    mon_close = serializers.TimeField(format='%H:%M', )
    tue_open = serializers.TimeField(format='%H:%M', )
    tue_close = serializers.TimeField(format='%H:%M', )
    wed_open = serializers.TimeField(format='%H:%M', )
    wed_close = serializers.TimeField(format='%H:%M', )
    thu_open = serializers.TimeField(format='%H:%M', )
    thu_close = serializers.TimeField(format='%H:%M', )
    fri_open = serializers.TimeField(format='%H:%M', )
    fri_close = serializers.TimeField(format='%H:%M', )
    sat_open = serializers.TimeField(format='%H:%M', )
    sat_close = serializers.TimeField(format='%H:%M', )
    sun_open = serializers.TimeField(format='%H:%M', )
    sun_close = serializers.TimeField(format='%H:%M', )

    class Meta:
        model = ScheduleModel
        fields = ('id', 'title', 'shop', 'mon_open', 'mon_close', 'tue_open', 'tue_close',
                  'wed_open', 'wed_close', 'thu_open', 'thu_close', 'fri_open', 'fri_close',
                  'sat_open', 'sat_close', 'sun_open', 'sun_close')
