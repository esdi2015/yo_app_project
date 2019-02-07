from django.conf.urls import re_path, include, url
from rest_framework import routers
from .views import UserViewSet, Logout, UserMe, UserIsExists, google_oauth, facebook_oauth, \
    user_reset_password_request_token, user_reset_password_confirm, free_managers_view,twitter_login, verify_email_view,verified_view, UserChangePassword
from . import views as api_view
from django.urls import path

router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'users', UserViewSet, base_name='UserView')

urlpatterns = router.urls

urlpatterns += [
    url(r'^registration/$', api_view.register_view, name='user_registration'),
    url(r'^login/$', api_view.login_view, name='user_login'),
    url(r'^logout/', Logout.as_view(), name='user_logout'),
    url(r'^user/me/', UserMe.as_view(), name='user_me'),
    url(r'^user/exists/', UserIsExists.as_view(), name='user_exists'),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^login-google/$', google_oauth, name='google_login'),
    url(r'^login-facebook/$',facebook_oauth , name='facebook_login'),
    #url(r'^password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    url(r'^password-reset/$', user_reset_password_request_token, name='reset_password_request'),
    url(r'^password-reset/confirm/$', user_reset_password_confirm, name='reset_password_confirm'),
    url(r'^verify-email/(?P<key>\w+)/$', verify_email_view, name='verify_email_view'),
    #url(r'^password-reset/confirm/', include('django_rest_passwordreset.urls', namespace='password_reset_confirm')),
    #url(r'^forgot-password/$', api_view.login_view, name='user_forgot_password'),
    url(r'^free-managers/', free_managers_view, name='free_managers'),
    url(r'^login-twitter/', twitter_login),
    url(r'^verified/', verified_view),
    url(r'^change-password/(?P<pk>\d+)/', UserChangePassword.as_view()),

]