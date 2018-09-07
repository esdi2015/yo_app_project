from django.apps import apps
from rest_framework import serializers


CityModel = apps.get_model('common', 'City')


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CityModel
        fields = ('id', 'city_name', )