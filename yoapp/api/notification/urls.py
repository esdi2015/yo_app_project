from django.conf.urls import  url
from .views import test_func,get_notifications,subscribe, unsubscribe,get_subscription,read_notification
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet

urlpatterns = [
    url(r'^reg-device/fcm/$',GCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='reg_fcm_device'),
    url(r'^get-notifications/$', get_notifications, name='get_notifications'),
    url(r'^subscribe/$', subscribe, name='subscribe'),
    url(r'^unsubscribe/$', unsubscribe, name='unsubscribe'),
    url(r'^get-subscription/$', get_subscription, name='get_subscription'),
    url(r'^read-notification/$', read_notification, name='read_notification'),

]