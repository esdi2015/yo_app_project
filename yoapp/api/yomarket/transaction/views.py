from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
# from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from ...utils import ERROR_API, PAYMENT_ERRORS
from yoapp.settings import TRANZILLA_PW,TRANZILLA_TERMINAL
from ...views import custom_api_response
from .serializers import TransactionSerializer,MyTransactionSerializer,\
                         CardHolderSerializer, CardHolderCreateSerializer,\
                         CheckoutSerializer, OrderListSerializer
from rest_framework import generics
from yomarket.models import Transaction ,CardHolder, Offer,CartProduct,OrderProduct,Order,Shop
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

@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
def make_payment(request):

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
        serializer = CardHolderCreateSerializer(data=request.data,context={'user':self.request.user})
        if serializer.is_valid():
            card_number=serializer.validated_data['card_number']
            exp_date = serializer.validated_data['exp_date']

            url = 'https://secure5.tranzila.com/cgi-bin/tranzila71u.cgi'
            params = {
                "supplier": TRANZILLA_TERMINAL,
                "TranzilaPW": TRANZILLA_PW,
                "ccno": card_number,
                "TranzilaTK": 1,
            }
            r = requests.get(url, params=params)
            token = r.text.strip().split(sep="=")[1]

            url = 'https://secure5.tranzila.com/cgi-bin/tranzila71u.cgi'
            params = {
                "supplier": TRANZILLA_TERMINAL,
                "TranzilaPW": TRANZILLA_PW,
                "expdate": "11/21",
                "TranzilaTK": token,
                'tranmode': 'V',
                'sum': 0.01,
                'cred_type': 1,
                'cy': 1,
                    }
            r = requests.get(url, params=params)
            response = dict(x.split('=') for x in r.text.split('&'))

            if response['Response']=='000':
                holder = CardHolder.objects.filter(tranzila_tk=token,exp_date=exp_date,user=self.request.user)
                if holder.exists():
                    error = {"detail": ERROR_API['125'][1]}
                    error_codes = [ERROR_API['125'][0]]
                    return Response(custom_api_response(errors=error, error_codes=error_codes),status=status.HTTP_400_BAD_REQUEST)
                else:
                    holder=CardHolder(user=request.user,exp_date=exp_date,tranzila_tk=token)
                    holder.save()
                    serializer =self.get_serializer(holder)
                    return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED, )
            else:
                error = {"payment_error_code":PAYMENT_ERRORS[response['Response']][0],"detail": PAYMENT_ERRORS[response['Response']][1]}
                error_codes = [ERROR_API['900'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {"detail": ERROR_API['164'][1]}
            error_codes = [ERROR_API['164'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_200_OK)



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




class CheckoutOrderView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def pay(self,cardholder,total):
        url = 'https://secure5.tranzila.com/cgi-bin/tranzila71u.cgi'
        params = {
            "supplier": TRANZILLA_TERMINAL,
            "TranzilaPW": TRANZILLA_PW,
            "expdate": cardholder.exp_date.strftime("%m%y"),
            "TranzilaTK": cardholder.tranzila_tk,
            'sum': total,
            'cred_type': 1,
            'cy': 1,}

        r = requests.get(url, params=params)
        response = dict(x.split('=') for x in r.text.split('&'))

        if response['Response'] == '000':
            return True
        else:
            error = {"payment_error_code": PAYMENT_ERRORS[response['Response']][0],
                     "detail": PAYMENT_ERRORS[response['Response']][1]}
            error_codes = [ERROR_API['900'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

    def get_total_sum(self,cart_products):
        total = 0
        for cart_product in cart_products:
            total = (cart_product.offer.price * cart_product.quantity)
        return total

    def make_order_products(self,cart_products,order):
        order_products=[]
        for cart_product in cart_products:
            product=OrderProduct(order=order,offer=cart_product.offer,
                                 quantity=cart_product.quantity)
        return order_products

    def save_order_products(self,order_products):
        for order_product in order_products:
            order_product.save()

    def get_cardholder(self,cardholder_id):
        try:
            cardholder = CardHolder.objects.get(pk=cardholder_id)
            if cardholder.user.pk==self.request.user.pk:
                return cardholder
            else:
                error = {"detail": ERROR_API['127'][1]}
                error_codes = [ERROR_API['127'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)
        except CardHolder.DoesNotExist:
            error = {"detail": ERROR_API['165'][1]}
            error_codes = [ERROR_API['165'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

    def delete_cart_products(self,cart_products):
        for cart_product in cart_products:
            cart_product.delete()


    def get_shop(self,shop_id):
        try:
            shop = Shop.objects.get(pk=shop_id)
            return shop
        except Shop.DoesNotExist:
            error = {"detail": ERROR_API['251'][1]}
            error_codes = [ERROR_API['251'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer=CheckoutSerializer(data=request.data)
        if serializer.is_valid():

            cart_product_ids = serializer.validated_data['cart_product_ids']
            cardholder_id = serializer.validated_data['cardholder_id']
            total_sum = serializer.validated_data['total_sum']
            shop_id = serializer.validated_data['shop_id']

            cart_products = CartProduct.objects.filter(pk__in=cart_product_ids)

            total = self.get_total_sum(cart_products)
            if total!=total_sum:
                error = {"detail": ERROR_API['901'][1]}
                error_codes = [ERROR_API['901'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)



            shop = self.get_shop(shop_id)

            order=Order(shop=shop,user=request.user,total_sum=total,status='PAID')

            cardholder = self.get_cardholder(cardholder_id)

            paid = self.pay(cardholder,total)

            if paid==True:
                order.save()
                self.save_order_products()
                self.delete_cart_products(cart_products)

                serializer = OrderListSerializer(order, context={'request': request})
                return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

        else:
            error = {"detail": ERROR_API['163'][1]}
            error_codes = [ERROR_API['163'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)


class OrderView(generics.ListAPIView,generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method=='GET':
            serializer = OrderListSerializer

        return serializer

    def get_queryset(self):
        if self.request.user.role=="CUSTOMER":
            orders = Order.objects.filter(user__pk=self.request.user.pk)
            return orders
        if self.request.user.role=="MANAGER":
            orders = Order.objects.filter(shop__manager__pk=self.request.user.pk)
            return orders
        if self.request.user.role=="OWNER":
            orders = Order.objects.filter(shop__user__pk=self.request.user.pk)



    def list(self, request, *args, **kwargs):
        serializer=self.get_serializer(self.get_queryset(),many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer=OrderListSerializer(instance=instance,data=request.data,partial=True)
        if serializer.is_valid():
            instance=serializer.save()
            serializer=OrderListSerializer(instance,context={'request':request})
            return Response(custom_api_response(serializer), status=status.HTTP_200_OK )
        else:
            error = {"detail": ERROR_API['163'][1]}
            error_codes = [ERROR_API['163'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def test_view(request):
    print(request.body)
    print(request.POST)
    print(request.GET)
    return HttpResponse('ok')