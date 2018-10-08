from django.conf.urls import re_path, include, url
from .views import OnboardingOfferListView,UserPreferencesTableCreateView,UserDataCreateView
urlpatterns = [
    url(r'^onboarding/offers/$', OnboardingOfferListView.as_view(), name='onboarding_list_views'),
    url(r'^user-preferences/create/$', UserPreferencesTableCreateView.as_view()),
    url(r'^user-preferences/data/create/$', UserDataCreateView.as_view()),

]