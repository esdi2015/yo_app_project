from django.conf.urls import  url
from .views import is_liked, like, unlike,list_like

urlpatterns = [
    url(r'^wish/is-liked/(?P<offer_id>\d{1,})$',is_liked, name='is_liked'),
    url(r'^wish/like/$', like, name='like'),
    url(r'^wish/unlike/$', unlike, name='unlike'),
    url(r'^wish/list-like/$', list_like, name='list-like'),

]