from django.conf.urls import re_path, include, url
from .views import OfferListView, OfferDetailView , CartView
from . import views as api_view


urlpatterns = [
    url(r'^offers/$', OfferListView.as_view(), name='offer-list'),
    url(r'^offers/(?P<pk>\d+)/$', OfferDetailView.as_view(), name='offer-detail'),
    url(r'^shopping-cart/$', CartView.as_view(), name='offer-detail')
]