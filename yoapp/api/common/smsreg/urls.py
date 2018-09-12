from django.conf.urls import re_path, include, url
from .views import Register,Verify

urlpatterns = [
    url(r'^sms-reg/register/$', Register, name='register'),
    url(r'^sms-reg/verify/$', Verify, name='verify'),

]