from django.conf.urls import  url
from .views import SecondaryInfoListCreateView, SecondaryInfoDetailView

urlpatterns = [

    url(r'^secondary-info/$', SecondaryInfoListCreateView.as_view(),name='secondary-info'),
    url(r'^secondary-info/(?P<pk>\d+)/$', SecondaryInfoDetailView.as_view(), name='secondary-info-detail'),

]

