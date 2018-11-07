import sys
sys.path.append("..")

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.apps import apps
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.password_validation import validate_password as vp


UserModel = get_user_model()
CategoryModel = apps.get_model('common', 'Category')
OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')


class MultipartM2MField(serializers.Field):
    def to_representation(self, obj):
        return obj.values_list('id', flat=True).order_by('id')

    def to_internal_value(self, data):
        if isinstance(data, list):
            return data if len(data) > 0 else None
        else:
            data = data.strip('[]')
            return data.split(',') if data else None





