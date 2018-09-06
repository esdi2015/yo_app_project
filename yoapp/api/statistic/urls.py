from django.conf.urls import  url
from .views import StatisticList
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet

urlpatterns = [
     url(r'^statistic/coupons/$',StatisticList.as_view(), name='count_view'),

]

