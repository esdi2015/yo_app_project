from django.conf.urls import re_path, include, url
from .views import ShopViewSet  # ShopList,
from . import views as api_view
from rest_framework import routers


router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'shops', ShopViewSet, base_name='ShopView')

urlpatterns = router.urls

urlpatterns += [
    #url(r'^shops/$', ShopList.as_view(), name='shop-list'),
    #url(r'^shops/(?P<pk>[^/.]+)/$', ShopList.as_view(), name='shop-detail'),
]