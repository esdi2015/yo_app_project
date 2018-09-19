from django.apps import apps
from rest_framework import serializers


ScheduleModel = apps.get_model('yomarket', 'Schedule')


class ScheduleSerializer(serializers.ModelSerializer):
    # customer = serializers.StringRelatedField()
    # customer_id = serializers.IntegerField(allow_null=False)
    # manager = serializers.StringRelatedField()
    # manager_id = serializers.IntegerField(allow_null=False)
    # offer = serializers.StringRelatedField()
    # offer_id = serializers.IntegerField(allow_null=False)
    # points = serializers.IntegerField(allow_null=False, default=0, required=False)

    class Meta:
        model = ScheduleModel
        fields = ('id', 'title', 'mon_open', 'mon_close', 'tue_open', 'tue_close',
                  'wed_open', 'wed_close', 'thu_open', 'thu_close', 'fri_open', 'fri_close',
                  'sat_open', 'sat_close', 'sun_open', 'sun_close')
