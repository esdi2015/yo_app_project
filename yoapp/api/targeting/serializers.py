from django.apps import apps
from rest_framework import serializers
from targeting.models import UserPreferencesTable,UserDataTable

class UserPreferencesTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPreferencesTable
        fields = ('data','user','object_type','object_id','created')



class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDataTable
        fields = ('birth_date','checkbox1','checkbox2')



