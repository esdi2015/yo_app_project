from django.conf.urls import re_path, include, url
from .views import TransactionViewSet
from . import views as api_view
from rest_framework import routers


router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'transactions', TransactionViewSet, base_name='TransactionView')

urlpatterns = router.urls
