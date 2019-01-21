from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
# from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from ...utils import ERROR_API

from ...views import custom_api_response
from .serializers import TransactionSerializer,MyTransactionSerializer,CardHolderSerializer
from rest_framework import generics
from yomarket.models import Transaction ,CardHolder, Offer
from api.views import CustomPagination, prepare_paginated_response
from rest_framework.decorators import api_view, permission_classes


TransactionModel = apps.get_model('yomarket', 'Transaction')


class TransactionListFilter(FilterSet):
    manager_ids = CharFilter(method='filter_manager_ids')
    offer_ids = CharFilter(method='filter_offer_ids')

    class Meta:
        model = TransactionModel
        fields = ('manager_id', 'offer_id', 'manager_ids', 'offer_ids')

    def filter_manager_ids(self, queryset, name, value):
        if value:
            queryset = queryset.filter(manager_id__in=value.strip().split(',')).all()
        return queryset

    def filter_offer_ids(self, queryset, name, value):
        if value:
            queryset = queryset.filter(offer_id__in=value.strip().split(',')).all()
        return queryset


class MyTransactionView(generics.ListAPIView):
    serializer_class = MyTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        customer = self.request.user
        queryset = Transaction.objects.filter(customer=customer)
        return queryset

    def list(self,request, *args, **kwargs):
        queryset=self.get_queryset()

        if queryset.exists():
            serilizer=self.get_serializer(queryset,many=True)
            return Response(custom_api_response(serilizer),status=status.HTTP_200_OK)
        error = {"detail": ERROR_API['203'][1]}
        error_codes = [ERROR_API['203'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)


class ManagerTransactionView(generics.ListAPIView):
    serializer_class = MyTransactionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filter_class = TransactionListFilter

    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('offer__title', )
    ordering_fields = ('points', 'created', 'offer__title', 'manager__email', 'customer__email', )

    def get_queryset(self):
        if self.request.user.role == 'MANAGER':
            queryset = Transaction.objects.filter(manager=self.request.user)
        elif self.request.user.role == 'OWNER':
            queryset = Transaction.objects.filter(offer__shop__user=self.request.user)
        else:
            queryset = None
        return queryset

    def list(self,request, *args, **kwargs):
        queryset=self.get_queryset()
        queryset = self.filter_queryset(queryset)

        if queryset.exists():
            paginate = prepare_paginated_response(self, request, queryset)
            if paginate:
                return Response(custom_api_response(content=paginate.content, metadata=paginate.metadata),
                                status=status.HTTP_200_OK)

            serilizer=self.get_serializer(queryset, many=True)
            return Response(custom_api_response(serilizer), status=status.HTTP_200_OK)
        else:
            error = {"detail": ERROR_API['203'][1]}
            error_codes = [ERROR_API['203'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)



class TransactionViewSet(viewsets.ModelViewSet):
    queryset = TransactionModel.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = CustomPagination
    filter_class = TransactionListFilter

    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('offer__title', )
    ordering_fields = ('points', 'created', 'offer__title', 'manager__email', 'customer__email', )

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return [IsAuthenticated(), ]
        else :
            return []

    def retrieve(self, request, pk=None):
        queryset = TransactionModel.objects.filter(pk=pk).all()
        serializer = TransactionSerializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        if queryset.exists():
            paginate = prepare_paginated_response(self, request, queryset)
            if paginate:
                return Response(custom_api_response(content=paginate.content, metadata=paginate.metadata),
                                status=status.HTTP_200_OK)

            # page_num = request.GET.get('page', None)
            # if page_num:
            #     page = self.paginate_queryset(queryset)
            #     if page is not None:
            #         serializer = self.get_serializer(page, many=True, context={'request': request})
            #         paginated_response = self.get_paginated_response(serializer.data)
            #         content = paginated_response.data['results']
            #         del paginated_response.data['results']
            #         metadata = paginated_response.data
            #         return Response(custom_api_response(content=content, metadata=metadata), status=status.HTTP_200_OK)

            serilizer=self.get_serializer(queryset, many=True)
            return Response(custom_api_response(serilizer), status=status.HTTP_200_OK)
        else:
            error = {"detail": ERROR_API['203'][1]}
            error_codes = [ERROR_API['203'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)


import requests

@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def make_payment(request):
    # cardholder_id = request.data.get('cardholder_id')
    # offer_id = request.data.get('offer_id')
    #
    #
    #
    # if cardholder_id == None or offer_id == None:
    #     error = {"detail": ERROR_API['163'][1]}
    #     error_codes = [ERROR_API['163'][0]]
    #     return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_200_OK)
    #
    #
    #
    #
    # try:
    #     offer = Offer.objects.get(id=offer_id)
    # except Offer.DoesNotExist:
    #     error = {"detail": ERROR_API['204'][1]}
    #     error_codes = [ERROR_API['204'][0]]
    #     return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_200_OK)
    #
    #
    #
    # try:
    #     card = CardHolder.objects.get(id=cardholder_id)
    # except CardHolder.DoesNotExist:
    #     error = {"detail": ERROR_API['165'][1]}
    #     error_codes = [ERROR_API['165'][0]]
    #     return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_200_OK)
    #
    #
    #
    #
    # if card.user != request.user:
    #     error = {"detail": ERROR_API['164'][1]}
    #     error_codes = [ERROR_API['164'][0]]
    #     return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_200_OK)
    #
    #
    #

    url = 'https://secure5.tranzila.com/cgi-bin/tranzila71u.cgi'
    params = {
        "supplier": 'yoo',
        "TranzilaPW":'We19ba1',
        "ccno":"5355074017294831",
        "TranzilaTK": 1,
    }

    r = requests.get(url, params=params)

    print(r.headers)
    print(r.content)
    print(r)



    return Response('ok')



class CardHolderViewSet(viewsets.ModelViewSet):
    serializer_class = CardHolderSerializer


    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset =CardHolder.objects.filter(user=self.request.user)
            return queryset
        else:
            queryset = None
            return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            error = {"detail": ERROR_API['165'][1]}
            error_codes = [ERROR_API['165'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context={'user':self.request.user})
        serializer.is_valid(raise_exception=True)
        holder = CardHolder.objects.filter(**serializer.data,user=self.request.user)
        if holder.exists():
            error = {"detail": ERROR_API['125'][1]}
            error_codes = [ERROR_API['125'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),status=status.HTTP_400_BAD_REQUEST)
        else:
            holder=serializer.save()
            serializer =self.get_serializer(holder)
            return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED, )

    def destroy(self, request, *args, **kwargs):
         instance = self.get_object()
         if self.request.user == instance.user:
             instance.delete()
             error = {"detail": ERROR_API['500'][1]}
             error_codes = [ERROR_API['500'][0]]
             return Response(custom_api_response(errors=error, error_codes=error_codes),status=status.HTTP_200_OK)
         else:
             error = {"detail": ERROR_API['164'][1]}
             error_codes = [ERROR_API['164'][0]]
             return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_200_OK)

