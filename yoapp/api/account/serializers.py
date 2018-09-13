from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.compat import authenticate

from account.models import Profile


UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    #first_name = serializers.SlugRelatedField(slug_field='user.first_name', read_only=True, required=False)
    #last_name = serializers.SlugRelatedField(slug_field='user.last_name', read_only=True, required=False)
    #user_id = serializers.IntegerField(allow_null=False)

    # def update(self, instance, validated_data):
    #     #instance.test = validated_data.get('test', instance.test)
    #     instance.date_birth = validated_data.get('date_birth', instance.date_birth)
    #     instance.photo = validated_data.get('photo', instance.photo)
    #     instance.save()
    #     return instance

    class Meta:
        model = Profile
        fields = ('user', 'user_id', 'date_birth', 'photo', 'gender') #, 'first_name', 'last_name'