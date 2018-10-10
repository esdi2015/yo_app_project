from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
# from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from ...utils import ERROR_API

from ...views import custom_api_response
from .serializers import TransactionSerializer,MyTransactionSerializer
from rest_framework import generics
from yomarket.models import Transaction


TransactionModel = apps.get_model('yomarket', 'Transaction')


# class ShopList(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request, format=None):
#         shops = ShopModel.objects.all()
#         serializer = ShopSerializer(shops, many=True)
#         return Response(custom_api_response(serializer), status=status.HTTP_200_OK)




class MyTransactionView(generics.ListAPIView):
    serializer_class = MyTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        customer = self.request.user
        queryset = Transaction.objects.filter(customer=customer)
        return queryset

    def list(self,request, *args, **kwargs):
        queryset=self.get_queryset()
        # print(queryset)
        if queryset.exists():
            serilizer=self.get_serializer(queryset,many=True)
            return Response(custom_api_response(serilizer),status=status.HTTP_200_OK)
        error = {"detail": ERROR_API['203'][1]}
        error_codes = [ERROR_API['203'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)


class ManagerTransactionView(generics.ListAPIView):
    serializer_class = MyTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.role == 'MANAGER':
            queryset = Transaction.objects.filter(manager=self.request.user)
        elif self.request.user.role == 'OWNER':
            queryset = Transaction.objects.filter(offer__shop__user=self.request.user)
        else:
            queryset=None


        return queryset

    def list(self,request, *args, **kwargs):
        queryset=self.get_queryset()
        if queryset==None:
            error = {"detail": ERROR_API['203'][1]}
            error_codes = [ERROR_API['203'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)
        if queryset.exists():
            serilizer=self.get_serializer(queryset,many=True)
            return Response(custom_api_response(serilizer),status=status.HTTP_200_OK)



class TransactionViewSet(viewsets.ModelViewSet):
    queryset = TransactionModel.objects.all()
    serializer_class = TransactionSerializer
    # permission_classes = (AllowAny,)

    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('offer__title', )
    # filter_fields = ('manager_id', )
    # ordering_fields = '__all__'
    ordering_fields = ('points', 'created', 'offer__title', 'manager__email', 'customer__email', )

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return [AllowAny(), ]  # AllowAny(), - remove it later, need to add  IsAuthenticated() !!!
        else :
            return []

    def retrieve(self, request, pk=None):
        queryset = TransactionModel.objects.filter(pk=pk).all()
        serializer = TransactionSerializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):

        # if (request.user.is_authenticated == True) and (request.user.role == 'OWNER'):
        #     queryset = ShopModel.objects.filter(user_id=request.user.pk).all()
        # else:
        #     queryset = ShopModel.objects.all()

        #queryset = self.filter_queryset(self.queryset)
        #queryset = TransactionModel.objects.all()
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #serializer = self.get_serializer(queryset, many=True)
        #serializer = TransactionSerializer(queryset, many=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
    #
    #
    # def create(self, request, *args, **kwargs):
    #     request.data['user_id'] = request.user.pk
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED, headers=headers)
    #
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     request.data['user_id'] = request.user.pk
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(custom_api_response(serializer), status=status.HTTP_200_OK)