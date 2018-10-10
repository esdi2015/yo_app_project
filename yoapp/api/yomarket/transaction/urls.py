from django.conf.urls import re_path, include, url
from .views import TransactionViewSet, MyTransactionView,ManagerTransactionView
from . import views as api_view
from rest_framework import routers


router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'transactions', TransactionViewSet, base_name='TransactionView')


urlpatterns = [
    url(r'^my-transactions/$', MyTransactionView.as_view(), name='my_transactions'),
    url(r'^manager-transactions/$', ManagerTransactionView.as_view()),

]

urlpatterns = router.urls + urlpatterns
