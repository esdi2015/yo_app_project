from django.conf.urls import  url
from .views import BusinessRequest


urlpatterns = [
    url(r'^business-registration/$', BusinessRequest.as_view()),
]