from django.conf.urls import  url
from .views import is_liked, like, unlike,MyCouponsListView
urlpatterns = [
    url(r'^wish/is-liked/(?P<offer_id>\d{1,})$',is_liked, name='is_liked'),
    url(r'^wish/like/$', like, name='like'),
    url(r'^wish/unlike/$', unlike, name='unlike'),
    url(r'^wish/list-like/$', MyCouponsListView.as_view(), name='list-like'),

]