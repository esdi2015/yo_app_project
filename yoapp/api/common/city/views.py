from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ...views import custom_api_response
from .serializers import CitySerializer


CityModel = apps.get_model('common', 'City')


class CityList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        categories = CityModel.objects.all()
        serializer = CitySerializer(categories, many=True)
        response = Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        return response
