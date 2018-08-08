from django.conf.urls import re_path, include, url
from rest_framework import routers
from .views import UserViewSet, Logout, UserMe, UserIsExists
from . import views as api_view


router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'users', UserViewSet, base_name='UserView')

urlpatterns = router.urls

urlpatterns += [
    url(r'^registration/$', api_view.register_view, name='user_registration'),
    url(r'^login/$', api_view.login_view, name='user_login'),
    url(r'^logout/', Logout.as_view(), name='user_logout'),
    url(r'^user/profile/', api_view.profile_update_view, name='user_profile_update'),
    url(r'^user/me/', UserMe.as_view(), name='user_me'),
    url(r'^user/exists/', UserIsExists.as_view(), name='user_exists'),
]