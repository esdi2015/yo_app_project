from django.conf.urls import re_path, include, url
from .views import OfferListView, OfferDetailView , ShoppingCartView, offer_search_view
from . import views as api_view


urlpatterns = [
    url(r'^offers/$', OfferListView.as_view(), name='offer-list'),
    url(r'^offers/(?P<pk>\d+)/$', OfferDetailView.as_view(), name='offer-detail'),
    url(r'^offers/search/$', offer_search_view, name='offer-search'),

    url(r'^shopping-cart/$', ShoppingCartView.as_view(), name='shopping-cart'),

]