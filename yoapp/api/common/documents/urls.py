from django.conf.urls import re_path, include, url
from .views import  terms_template_view

urlpatterns = [
    url(r'^documents/terms/$', terms_template_view),
]