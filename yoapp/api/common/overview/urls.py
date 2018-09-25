from django.conf.urls import  url
from .views import overview_view

urlpatterns = [
    url(r'^overview/$', overview_view)


]

