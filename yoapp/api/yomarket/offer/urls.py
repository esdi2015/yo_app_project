from django.conf.urls import re_path, include, url
from .views import OfferList, OfferSearchView
from . import views as api_view


urlpatterns = [
    url(r'^offers/$', OfferList.as_view(), name='offer-list'),
    url(r'^offers/(?P<pk>\d+)/$', OfferList.as_view(), name='offer-detail'),
    url(r'^offers/search/', OfferSearchView.as_view(), name='offer-search'),
]