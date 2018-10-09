from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.compat import authenticate

from account.models import Profile


UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    first_name = serializers.StringRelatedField(source='user.first_name')
    last_name = serializers.StringRelatedField(source='user.last_name')

    # def update(self, instance, validated_data):
    #     # instance.test = validated_data.get('test', instance.test)
    #     # instance.date_birth = validated_data.get('date_birth', instance.date_birth)
    #     # instance.photo = validated_data.get('photo', instance.photo)
    #     # instance.save()
    #     # return instance

    class Meta:
        model = Profile
        fields = ('user', 'user_id', 'date_birth', 'photo', 'gender',
                  'points', 'rank', 'region', 'interests',
                  'first_name', 'last_name', 'phone', 'payment_method', 'subscribe')


class ProfilePhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = Profile
        fields = ('photo', )



