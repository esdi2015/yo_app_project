from django.shortcuts import render, HttpResponseRedirect
from django.apps import apps
from rest_framework import viewsets
from rest_framework import generics
from django.shortcuts import get_object_or_404
#from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView


from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, mixins
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.apps import apps

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework.pagination import LimitOffsetPagination

from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.core.exceptions import ObjectDoesNotExist

from rest_auth.models import TokenModel
from rest_auth.app_settings import create_token
from rest_framework.views import exception_handler



UserModel = get_user_model()
CategoryModel = apps.get_model('common', 'Category')
OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    try:
        detail = response.data.get('detail')
    except Exception as e:
        detail = e
    if response is not None:
        if detail:
            response.data['metadata'] = {}
            response.data['errors'] = {'non_field_errors': detail}
            del response.data['detail']

    return response


def custom_api_response(serializer=None, content=None, errors=None, metadata={}, error_codes=[]):
    api_error_codes = []
    if content:
        response = {'metadata': metadata, 'content': content}
        return response

    if errors:
        if len(error_codes) > 0:
            metadata = {'api_error_codes': error_codes}
        response = {'metadata': metadata, 'errors': errors}
        return response

    if not hasattr(serializer, '_errors') or len(serializer._errors) == 0:
        if hasattr(serializer, 'data'):
            response = {'metadata': metadata, 'content': serializer.data}
        else:
            response = {'metadata': metadata, 'content': 'unknown'}
    else:
        #print(serializer._errors)
        for key in serializer._errors.keys():
            try:
                api_error_codes.append(serializer._errors[key][0].code)
            except Exception as e:
                pass
        #if 'non_field_errors' in serializer._errors:
        if len(api_error_codes) > 0:
            metadata = {'api_error_codes': api_error_codes}
        response = {'metadata': metadata, 'errors': serializer._errors}
    return response




def get_error_code():
    return None






