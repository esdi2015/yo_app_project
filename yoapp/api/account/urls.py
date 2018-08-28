from django.conf.urls import re_path, include, url
from rest_framework import routers
from . import views as api_view

from .views import ProfileDetailView

# router = routers.DefaultRouter()
# router.include_format_suffixes = False
#router.register(r'shops', ShopViewSet, base_name='ShopView')

#urlpatterns = router.urls


urlpatterns = [
    url(r'^user/profile/', ProfileDetailView.as_view(), name='user_profile'),
]