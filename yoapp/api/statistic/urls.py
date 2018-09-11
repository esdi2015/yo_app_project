from django.conf.urls import  url
from .views import StatisticList,StatisticViewsList

urlpatterns = [
     url(r'^statistic/coupons/$',StatisticList.as_view(), name='coupons_statistic'),
     url(r'^statistic/views/$', StatisticViewsList.as_view(), name='views_statistic'),

]

