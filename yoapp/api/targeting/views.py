from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from django.contrib.auth import get_user_model

from ..views import custom_api_response
from api.yomarket.offer.serializers import OfferSerializer

from ..utils import ERROR_API

from .serializers import UserPreferencesTableSerializer,UserDataSerializer

OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')
UserModel = get_user_model()


class OnboardingOfferListView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]

    def get_queryset(self):
        queryset = OfferModel.objects.filter(available=True)[:10]
        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            error = {"detail": ERROR_API['204'][1]}
            error_codes = [ERROR_API['204'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)




class UserPreferencesTableCreateView(generics.ListCreateAPIView):
    serializer_class = UserPreferencesTableSerializer
    permission_classes = (IsAuthenticated,)


    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED)


class UserDataCreateView(generics.ListCreateAPIView):
    serializer_class = UserDataSerializer
    permission_classes = (IsAuthenticated,)


    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED)
