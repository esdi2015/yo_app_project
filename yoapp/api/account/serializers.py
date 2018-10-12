from django.utils.translation import ugettext_lazy as _
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.compat import authenticate
from rest_framework.utils import model_meta

from account.models import Profile
from api.common.user.serializers import CustomUserSerializer


UserModel = get_user_model()
Category = apps.get_model('common', 'Category')



class MultipartM2MField(serializers.Field):
    def to_representation(self, obj):
        return obj.values_list('id', flat=True).order_by('id')

    def to_internal_value(self, data):
        if isinstance(data, list):
            return data if len(data) > 0 else None
        else:
            data = data.strip('[]')
            return data.split(',') if data else None



class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    first_name = serializers.StringRelatedField(source='user.first_name')
    last_name = serializers.StringRelatedField(source='user.last_name')

    class Meta:
        model = Profile
        fields = ('user', 'user_id', 'date_birth', 'photo', 'gender',
                  'points', 'rank', 'region', 'interests', 'age',
                  'first_name', 'last_name', 'phone', 'payment_method', 'subscribe')





class ProfileUpdateSerializer(ProfileSerializer):
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    interests = MultipartM2MField(allow_null=True, required=False)

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                if attr == 'interests':
                    if value is None:
                        instance.interests.clear()
                    else:
                        try:
                            interests_data = Category.objects.filter(id__in=value).all()
                            field = getattr(instance, attr)
                            field.set(value)
                        except IntegrityError as e:
                            pass
                else:
                    field = getattr(instance, attr)
                    field.set(value)
            else:
                setattr(instance, attr, value)

        user_info = UserModel.objects.filter(pk=validated_data['user_id']).first()
        user_data = {'first_name': validated_data['first_name'] if 'first_name' in validated_data else user_info.first_name,
                     'last_name': validated_data['last_name'] if 'last_name' in validated_data else user_info.last_name}

        for attr, value in user_data.items():
            setattr(user_info, attr, value)

        instance.save()
        user_info.save()

        return instance


    def to_representation(self, instance):
        representation = super(ProfileUpdateSerializer, self).to_representation(instance)
        user_serializer = CustomUserSerializer(UserModel.objects.filter(id=representation['user_id']).first())
        representation['first_name'] = user_serializer.data['first_name']
        representation['last_name'] = user_serializer.data['last_name']
        return representation



class ProfilePhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = Profile
        fields = ('photo', )



