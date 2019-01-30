from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, BooleanFilter, CharFilter
from django.contrib.auth import get_user_model
import datetime
from django.db.models import Q
from api.views import CustomPagination, prepare_paginated_response
from ...views import custom_api_response
from .serializers import OfferSerializer,\
                        CartProductListSerializer,\
                        CartProductCreateSerializer,\
                        CartProductDeleteSerializer

from statistic.utlis import count_shown
from history.utils import history_view_event, history_offer_search_event
from ...utils import ERROR_API
from django.shortcuts import  get_object_or_404
from yomarket.models import QRcoupon,CartProduct

OfferModel = apps.get_model('yomarket', 'Offer')
ShopModel = apps.get_model('yomarket', 'Shop')
UserModel = get_user_model()


class OfferListFilter(FilterSet):
    is_expired = BooleanFilter(method='filter_is_expired')
    category_ids = CharFilter(method='filter_category_ids')
    shop_ids = CharFilter(method='filter_shop_ids')
    offer_type = CharFilter(method='filter_offer_type')
    offer_status = CharFilter(method='filter_offer_status')


    class Meta:
        model = OfferModel
        fields = ('category_id', 'shop_id', 'discount_type', 'offer_type', 'is_expired',
                  'category_ids', 'status', 'shop_ids')

    def filter_offer_status(self,queryset,name,value):
        if value:
            queryset = queryset.filter(status=value)
        return queryset

    def filter_category_ids(self, queryset, name, value):
        if value:
            queryset = queryset.filter(category_id__in=value.strip().split(',')).all()
        return queryset

    def filter_shop_ids(self, queryset, name, value):
        if value:
            queryset = queryset.filter(shop_id__in=value.strip().split(',')).all()
        return queryset

    def filter_is_expired(self, queryset, name, value):
        if value == False:
            queryset = queryset.filter(expire__gte=datetime.datetime.now())
        elif value == True:
            queryset = queryset.filter(expire__lt=datetime.datetime.now())
        return queryset

    def filter_offer_type(self, queryset, name, value):
        if value=='DAILY':
            queryset = queryset.filter(offer_type=value).all()[:1]
            return queryset
        elif value=='REGULAR':
            queryset = queryset.filter(offer_type=value).all()
            return queryset


class OfferListView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    filter_class = OfferListFilter
    pagination_class = CustomPagination

    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('description', 'title')
    ordering_fields = ('shop__title', 'category__category_name', 'title', 'image',
                       'short_description', 'price', 'offer_type', 'expire', 'codes_count',
                       'redeemed_codes_count', 'status')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]


    def get_queryset(self):
        if self.request.user.is_anonymous:
            queryset = OfferModel.objects.filter(expire__gte=datetime.datetime.now())

            return queryset

        if (self.request.user.is_authenticated == True) and (self.request.user.role in ['MANAGER', 'OWNER']):
            queryset = OfferModel.objects.all()

        if self.request.user.is_authenticated == True and self.request.user.role == 'CUSTOMER':
            queryset = OfferModel.objects.filter(expire__gte=datetime.datetime.now())
            # good_ids=[]
            # for each in queryset:
            #     try:
            #         coupon = QRcoupon.objects.get(is_redeemed=False, is_expired=False,user_id=self.request.user, offer=each)
            #     except QRcoupon.DoesNotExist:
            #         good_ids.append(each.id)
            # queryset = OfferModel.objects.filter(id__in=good_ids)

            targeting = self.request.query_params.get('targeting')

            if targeting == 'true':


                if not self.request.user.profile.interests.exists():
                    empty_list=[]
                    return queryset,empty_list
                else:
                    target_categs = self.request.user.profile.interests.all()
                    target_ids = []

                    for each in target_categs:
                        set = OfferModel.objects.filter(category=each, available=True,offer_type='REGULAR',expire__gte=datetime.datetime.now())[:5]
                        target_ids = target_ids + [x.id for x in set]

                    all_set = queryset.filter(offer_type='REGULAR').exclude(id__in=target_ids)
                    targeted_set = OfferModel.objects.filter(id__in=target_ids).order_by('?')
                    return all_set,targeted_set


        else:
            if self.request.user.is_authenticated == True and self.request.user.role == 'ADMIN':
                queryset = OfferModel.objects.all()

            queryset = OfferModel.objects.filter(expire__gte=datetime.datetime.now())

        return queryset


    def list(self, request, *args, **kwargs):

        targeting = self.request.query_params.get('targeting')

        if self.request.user.is_anonymous:
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)

        elif targeting=='true' and self.request.user.role=='CUSTOMER':
            all_set,targeted_set = self.get_queryset()
            queryset = list(targeted_set)+list(all_set)
            if queryset==[]:
                error = {"detail": ERROR_API['204'][1]}
                error_codes = [ERROR_API['204'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            queryset=self.get_queryset()
            queryset=self.filter_queryset(queryset)

        if request.user.is_authenticated == True:
            if request.user.role == 'OWNER':
                shops = ShopModel.objects.filter(user_id=request.user.pk).all()
            elif request.user.role == 'MANAGER':
                shops = ShopModel.objects.filter(manager_id=request.user.pk).all()

            if request.user.role in ['OWNER', 'MANAGER']:
                shops_ids = [x.id for x in shops]
                queryset = self.filter_queryset(self.get_queryset())
                queryset = queryset.filter(shop_id__in=shops_ids)



        if targeting != 'true':
            if not queryset.exists():
                try:
                    offer_type = self.request.GET['offer_type']
                except Exception as e:
                    offer_type = None

                if offer_type == 'DAILY':
                    error = {"detail": ERROR_API['205'][1]}
                    error_codes = [ERROR_API['205'][0]]
                elif offer_type == 'REGULAR':
                    error = {"detail": ERROR_API['206'][1]}
                    error_codes = [ERROR_API['206'][0]]
                else:
                    error = {"detail": ERROR_API['204'][1]}
                    error_codes = [ERROR_API['204'][0]]

                return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

        category_id = request.query_params.get('category_id')
        if category_id != None:
            history_view_event(obj=category_id,user=request.user)

        search_text = request.query_params.get('search')
        if search_text != None:
            if request.user.is_authenticated==True:
                history_offer_search_event(search_text,user=request.user)


        paginate = prepare_paginated_response(self, request, queryset)
        if paginate:
            return Response(custom_api_response(content=paginate.content, metadata=paginate.metadata), status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED, headers=headers)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfferModel.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            error = {"detail": ERROR_API['207'][1]}
            error_codes = [ERROR_API['207'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_404_NOT_FOUND)

        history_view_event(instance,user=request.user)
        count_shown(instance)
        serializer = self.get_serializer(instance)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


from rest_framework.decorators import api_view
@api_view(['GET',])
def offer_search_view(request):
    search_field = request.GET.get('search')
    if search_field != None:
        offers =OfferModel.objects.filter(Q(title__icontains=search_field) | Q(description__icontains=search_field) | Q(short_description__icontains=search_field))
        offers= offers.filter(status='PUBLISHED',available=True)
        if offers.exists():
            serializer = OfferSerializer(offers,many=True)
            return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
        else:
            error = {"detail": ERROR_API['207'][1]}
            error_codes = [ERROR_API['207'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_404_NOT_FOUND)
    else:
        error = {"detail": ERROR_API['163'][1]}
        error_codes = [ERROR_API['163'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes),
                        status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartView(generics.ListAPIView,generics.CreateAPIView,generics.UpdateAPIView,generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method=='POST':
            return CartProductCreateSerializer
        elif self.request.method == 'DELETE':
            return CartProductDeleteSerializer
        else:
            return CartProductListSerializer

    def get_queryset(self):
        cart_products = CartProduct.objects.filter(user=self.request.user)
        return cart_products


    def list(self, request, *args, **kwargs):
        cart_products = self.get_queryset()
        cart_products = cart_products.order_by('added_to_cart')
        if cart_products.exists():
            for cart_product in cart_products:
                if cart_product.offer.available == False :
                    cart_product.delete()
            cart_products = self.get_queryset()
            cart_products = cart_products.order_by('added_to_cart')
            if cart_products.exists():
                serializer = self.get_serializer(cart_products,many=True)
                return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
            else:
                error = {"detail": ERROR_API['210'][1]}
                error_codes = [ERROR_API['210'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {"detail": ERROR_API['210'][1]}
            error_codes = [ERROR_API['210'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            try:
                instance=CartProduct.objects.get(user=request.user,offer=serializer.validated_data['offer'])
                serializer.update(instance,serializer.validated_data)
            except CartProduct.DoesNotExist:
                cart = serializer.save()
        else:
            error = {"detail": ERROR_API['163'][1]}
            error_codes = [ERROR_API['163'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(custom_api_response(serializer=serializer), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            print(serializer.validated_data)

            cart_products_ids = serializer.validated_data['id']

            cart_products = CartProduct.objects.filter(pk__in=cart_products_ids)

            if cart_products.exists():
                for cart_product in cart_products:
                    cart_product.delete()

                error = {"detail": ERROR_API['500'][1]}
                error_codes = [ERROR_API['500'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_200_OK)


            else:
                error = {"detail": ERROR_API['163'][1]}
                error_codes = [ERROR_API['163'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)


            # try:
            #     instance = CartProduct.objects.get(user=request.user, offer=serializer.validated_data['offer'])
            #     instance.delete()
            #     error = {"detail": ERROR_API['500'][1]}
            #     error_codes = [ERROR_API['500'][0]]
            #     return Response(custom_api_response(errors=error, error_codes=error_codes),
            #                     status=status.HTTP_200_OK)
            # except CartProduct.DoesNotExist:
            #     error = {"detail": ERROR_API['163'][1]}
            #     error_codes = [ERROR_API['163'][0]]
            #     return Response(custom_api_response(errors=error, error_codes=error_codes),
            #                     status=status.HTTP_400_BAD_REQUEST)

        else:
            error = {"detail": ERROR_API['163'][1]}
            error_codes = [ERROR_API['163'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)

