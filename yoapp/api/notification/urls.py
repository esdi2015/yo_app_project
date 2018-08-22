from django.conf.urls import  url
from .views import test_func,get_notifications,subscribe, unsubscribe,get_subscription
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet

urlpatterns = [
    url(r'^reg-device/fcm/$',GCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='reg_fcm_device'),
    url(r'^reg-device/test/$', test_func, name='reg_fcm_device'),
    url(r'^get-notifications/$', get_notifications, name='get_notifications'),
    url(r'^subscribe/$', subscribe, name='subscribe'),
    url(r'^unsubscribe/$', unsubscribe, name='unsubscribe'),
    url(r'^get-subscription/$', get_subscription, name='get_subscription'),

]