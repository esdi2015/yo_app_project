from django.apps import apps
from rest_framework import serializers
from targeting.models import UserPreferencesTable,UserDataTable

class UserPreferencesTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPreferencesTable
        fields = ('data','user','object_type','object_id','created')

    def create(self, validated_data):
        instance = UserPreferencesTable(**validated_data, user=self.context['request'].user)
        instance.save()

        return instance


class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDataTable
        fields = ('user','age','gender','checkbox1','checkbox2')



    def create(self,validated_data):
          instance= UserDataTable(**validated_data,user=self.context['request'].user)
          instance.save()

          return instance
