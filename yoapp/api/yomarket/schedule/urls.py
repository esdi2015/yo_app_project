from django.conf.urls import re_path, include, url
from .views import ScheduleViewSet
from . import views as api_view
from rest_framework import routers


router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'schedules', ScheduleViewSet, base_name='ScheduleView')

urlpatterns = router.urls
