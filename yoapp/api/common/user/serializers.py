from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password as vp
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.compat import authenticate

from common.utils import ROLES, DEFAULT_USER_ROLE
from account.models import Profile


UserModel = get_user_model()

APP = ('desktop', 'mobile')


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(allow_blank=False, write_only=True)
    role = serializers.CharField(allow_blank=True, default=DEFAULT_USER_ROLE)
    creator_id = serializers.IntegerField(allow_null=True, write_only=True, required=False)
    username = serializers.CharField(allow_blank=True, required=False)

    # def validate(self, attrs):
    #     if attrs['password'] != attrs.pop('confirm_password'):
    #         raise serializers.ValidationError({'confirm_password':
    #                                                _('Passwords do not match')})
    #     return attrs

    def validate_password(self, value):
        vp(value)
        return value

    def validate_username(self, value):
        # method = self.context['request'].method
        try:
            pk = int(self.context['request'].parser_context['kwargs']['pk'])
        except:
            pk = None

        try:
            user = UserModel.objects.get(username=value)
        except UserModel.DoesNotExist:
            user = None

        if user:
            if user.pk != pk:
                raise serializers.ValidationError("user with this username already exists.")
            else:
                return value
        else:
            return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        #Profile.objects.create(user=user)
        return user

    class Meta:
        model = UserModel
        fields = ('id', 'password', 'username', 'first_name', 'last_name', 'email', 'role', 'creator_id')
        write_only_fields = ('password', )


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    app = serializers.CharField(allow_blank=True, required=False, default=APP[1])

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        app = attrs.get('app')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            else:
                if user.role == 'ADMIN':
                    msg = _('Unable to log in with ADMIN role.')
                    raise serializers.ValidationError(msg, code='authorization')
                else:
                    if user.role == 'CUSTOMER' and app == APP[0]:
                        msg = _('Unable to log in with CUSTOMER role.')
                        raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserIsExistsSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))

    def validate(self, attrs):
        email = attrs.get('email')

        if email:
            user = UserModel.objects.filter(email=email).all()

            if not user:
                msg = _('User does not exists')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "email".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        #instance.test = validated_data.get('test', instance.test)
        instance.date_birth = validated_data.get('date_birth', instance.date_birth)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance

    class Meta:
        model = Profile
        fields = ('date_birth', 'photo')