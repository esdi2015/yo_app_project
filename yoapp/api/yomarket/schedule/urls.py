from django.conf.urls import re_path, include, url
from .views import ScheduleListView, ScheduleDetailView
from . import views as api_view
from rest_framework import routers


# router = routers.DefaultRouter()
# router.include_format_suffixes = False
# router.register(r'schedules', ScheduleViewSet, base_name='ScheduleView')
#
# urlpatterns = router.urls


urlpatterns = [
    url(r'^schedules/$', ScheduleListView.as_view(), name='offer-list'),
    url(r'^schedules/(?P<pk>\d+)/$', ScheduleDetailView.as_view(), name='offer-detail'),
]
