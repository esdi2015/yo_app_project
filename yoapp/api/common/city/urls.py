from django.conf.urls import re_path, include, url
from .views import CityList
from . import views as api_view


urlpatterns = [
    url(r'^cities/$', CityList.as_view()),
]