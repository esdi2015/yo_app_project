from django.conf.urls import  url
from .views import MyHistoryView



urlpatterns = [
    url(r'^my-history/$', MyHistoryView.as_view(), name='my_history'),

]
