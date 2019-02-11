from django.conf.urls import re_path, include, url
from .views import TransactionViewSet, MyTransactionView,\
                    ManagerTransactionView , CardHolderViewSet,CheckoutOrderView,\
                    OrderView, test_view, CouponView, CouponSettingsListView,CouponSettingsDetailView
from . import views as api_view
from rest_framework import routers


router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'transactions', TransactionViewSet, base_name='TransactionView')


urlpatterns = [
    url(r'^my-transactions/$', MyTransactionView.as_view(), name='my_transactions'),
    url(r'^manager-transactions/$', ManagerTransactionView.as_view()),
    url(r'^cardholder/$', CardHolderViewSet.as_view({'get': 'list','post':'create','delete':'destroy'})),
    url(r'^cardholder/(?P<pk>\d+)/$', CardHolderViewSet.as_view({'delete': 'destroy'})),
    url(r'^pay/$', CheckoutOrderView.as_view()),
    url(r'^order/$', OrderView.as_view()),
    url(r'^order/(?P<pk>\d+)/$', OrderView.as_view()),
    url(r'^test/$', test_view),
    url(r'^coupons/$', CouponView.as_view()),
    url(r'^coupons-settings/$', CouponSettingsListView.as_view()),
    url(r'^coupons-settings/(?P<pk>\d+)/$', CouponSettingsDetailView.as_view()),

]

urlpatterns = router.urls + urlpatterns
