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
from yomarket.models import Transaction ,CardHolder, Offer,CartProduct,\
                            OrderProduct,Order,Shop,CouponSetting,Coupon
from api.views import CustomPagination, prepare_paginated_response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from yomarket.utils import recalculate_rank,send_invoice
from django.utils import timezone
TransactionModel = apps.get_model('yomarket', 'Transaction')
UserModel = get_user_model()


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

from django.shortcuts import redirect
from decimal import *
class CardHolderViewSet(viewsets.ModelViewSet):
    serializer_class = CardHolderSerializer
    permission_classes = (AllowAny,)


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
        response=request.POST['Response']

        if response=='000':
            tranzilaTK=request.POST['TranzilaTK']
            expmonth = request.POST['expmonth']
            expyear = request.POST['expyear']
            userid = request.POST['userid']

            user = UserModel.objects.get(pk=userid)

            holder = CardHolder.objects.filter(tranzila_tk=tranzilaTK, user=user)
            if holder.exists():
                error = {"detail": ERROR_API['125'][1]}
                error_codes = [ERROR_API['125'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST,headers={'error_code':ERROR_API['125'][0],
                                                                            'error_detail':ERROR_API['125'][1]})
            else:
                expyear = int(expyear)
                expmonth = int(expmonth)
                expyear = expyear + 2000
                expdate = datetime(day=1, month=expmonth, year=expyear)
                holder = CardHolder(user=user, exp_date=expdate, tranzila_tk=tranzilaTK)
                holder.save()
                error = {"detail": ERROR_API['500'][1]}
                error_codes = [ERROR_API['500'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_201_CREATED,headers={'success':True})
        else:
            error = {"payment_error_code": PAYMENT_ERRORS[response][0],
                     "detail": PAYMENT_ERRORS[response][1]}
            error_codes = [ERROR_API['900'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST,headers={'error_code':ERROR_API['900'][0],
                                                                        'payment_error_code':PAYMENT_ERRORS[response][0],
                                                                        'error_detail':PAYMENT_ERRORS[response][1]})



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
            return True,True
        else:
            error = {"payment_error_code": PAYMENT_ERRORS[response['Response']][0],
                     "detail": PAYMENT_ERRORS[response['Response']][1]}
            error_codes = [ERROR_API['900'][0]]
            return False,Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

    def get_total_sum(self,cart_products):
        total = Decimal()
        for cart_product in cart_products:
            total = total + (cart_product.offer.price * cart_product.quantity)
        return total

    def make_order_products(self,cart_products,order):
        order_products=[]
        for cart_product in cart_products:
            product=OrderProduct(order=order,offer=cart_product.offer,
                                 quantity=cart_product.quantity)
            order_products.append(product)
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

    def get_coupon(self,coupon_id):
        try:
            coupon = Coupon.objects.get(pk=coupon_id)
            return coupon
        except Coupon.DoesNotExist:
            error = {"detail": ERROR_API['200'][1]}
            error_codes = [ERROR_API['200'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)


    def get_discount_total(self,coupon,total):
        if coupon.discount_type=='ABSOLUTE':
            discount_total = total-coupon.discount
            return discount_total
        if coupon.discount_type=='PERCENT':
            percent_value = (total/100.00)*coupon.discount
            discount_total =total-percent_value
            return discount_total

    def create(self, request, *args, **kwargs):
        serializer=CheckoutSerializer(data=request.data)
        if serializer.is_valid():

            cart_product_ids = serializer.validated_data['cart_product_ids']
            cardholder_id = serializer.validated_data['cardholder_id']
            total_sum = serializer.validated_data['total_sum']
            discount_sum = serializer.validated_data.get('discount_sum')
            shop_id = serializer.validated_data['shop_id']
            coupon_id =serializer.validated_data.get('coupon_id')
            fullname =serializer.validated_data.get('fullname')
            phone =serializer.validated_data.get('phone')
            coupon_used=False

            cart_products = CartProduct.objects.filter(pk__in=cart_product_ids)
            points=0
            cardholder = self.get_cardholder(cardholder_id)
            if type(cardholder) == type(Response()):
                return cardholder
            if coupon_id!=None:
                if discount_sum==None:
                    error = {"detail": ERROR_API['902'][1]}
                    error_codes = [ERROR_API['902'][0]]
                    return Response(custom_api_response(errors=error, error_codes=error_codes),
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    coupon = self.get_coupon(coupon_id)
                    if type(coupon) == type(Response()):
                        return coupon
                    coupon_used = True
                    total = self.get_total_sum(cart_products)
                    if type(total) == type(Response()):
                        return total
                    discount_total = self.get_discount_total(coupon,total)
                    if type(discount_total) == type(Response()):
                        return discount_total
                    if discount_total != discount_sum:
                        error = {"detail": ERROR_API['901'][1]}
                        error_codes = [ERROR_API['901'][0]]
                        return Response(custom_api_response(errors=error, error_codes=error_codes),
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        shop = self.get_shop(shop_id)
                        if type(shop) == type(Response()):
                            return shop


                        order = Order(shop=shop,
                                      user=request.user,
                                      total_sum=discount_total,
                                      status='PAID',
                                      fullname=fullname,
                                      phone=phone,coupon=coupon)
                        order.save()
                        order_products=self.make_order_products(cart_products,order)

                        paid,response = self.pay(cardholder, discount_total)
                        points=discount_total

            else:
                total = self.get_total_sum(cart_products)
                if type(total) == type(Response()):
                    return total
                if float(total) != float(total_sum):
                    error = {"detail": ERROR_API['901'][1]}
                    error_codes = [ERROR_API['901'][0]]
                    return Response(custom_api_response(errors=error, error_codes=error_codes),
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    shop = self.get_shop(shop_id)
                    if type(shop) == type(Response()):
                        return shop
                    shop = self.get_shop(shop_id)
                    order = Order(shop=shop,
                                  user=request.user,
                                  total_sum=total,
                                  status='PAID',
                                  fullname=fullname,
                                  phone=phone)
                    order.save()

                    order_products=self.make_order_products(cart_products, order)
                    points=total
                    paid,response = self.pay(cardholder, total)
                    if type(paid) == type(Response()):
                        return paid


            if paid==True:
                order.save()
                self.save_order_products(order_products=order_products)
                self.delete_cart_products(cart_products)
                if coupon_used:
                    coupon.status='USED'
                    coupon.used = timezone.now()
                    coupon.order=order
                    coupon.save()
                send_invoice(order,request.user)
                self.request.user.profile.points=self.request.user.profile.points + int(points)
                self.request.user.profile.save()
                recalculate_rank(self.request.user)
                serializer = OrderListSerializer(order, context={'request': request})
                return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
            else:
                order.delete()
                return response

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







from  .serializers import CouponMakeSerilalizer,CouponCustomerListSerializer

class CouponView(generics.CreateAPIView,generics.ListAPIView):
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        if self.request.user.role=='CUSTOMER':
            if self.request.query_params.get('shopid')!=None:
                queryset = Coupon.objects.filter(user=self.request.user,
                                                 status='AVAILABLE',
                                                 shop__pk=int(self.request.query_params['shopid'])).order_by('shop')
                return queryset
            queryset = Coupon.objects.filter(user=self.request.user,status='AVAILABLE')
            return queryset

    def user_can_get_coupon(self,user, shop):
        settings = CouponSetting.objects.filter(rank__lte=user.profile.rank, shop=shop)
        can_get= False
        settings_list= list()
        for setting in settings:
            coupons_count = Coupon.objects.filter(setting=setting).count()
            if coupons_count < setting.coupons_per_user:
                settings_list.append(setting)
                can_get=True
        return can_get, settings_list



    def create(self, request, *args, **kwargs):
        serializer = CouponMakeSerilalizer(data=request.data)
        if serializer.is_valid():
            shop=serializer.validated_data['shop']
            can_get,settings=self.user_can_get_coupon(user=request.user,shop=shop)
            if can_get:
                coupons=list()
                for setting in settings:
                    coupon= Coupon(user=request.user,
                                   discount=setting.discount,
                                   discount_type=setting.discount_type,
                                   shop=setting.shop,
                                   setting=setting)
                    coupon.save()
                    coupons.append(coupon)

                serializer=CouponCustomerListSerializer(coupons,many=True,context={'request':self.request})
                return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
            else:
                error = {"detail": ERROR_API['211'][1]}
                error_codes = [ERROR_API['211'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)

        error = {"detail": ERROR_API['163'][1]}
        error_codes = [ERROR_API['163'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes),
                        status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if queryset.exists():
            queryset=queryset.order_by('shop')
            serializer = CouponCustomerListSerializer(queryset,many=True,context={'request':self.request})
            return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        else:
            error = {"detail": ERROR_API['200'][1]}
            error_codes = [ERROR_API['200'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yomarket.utils import recalculate_rank
@csrf_exempt
@api_view()
@permission_classes((IsAuthenticated, ))
def test_view(request):

    return  Response('ok',headers={'dsadsasad':'dsadsadassadsad'})



