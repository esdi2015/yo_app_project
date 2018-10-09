from django.conf.urls import url
from .views import ProfileDetailView, ProfilePhotoView

urlpatterns = [
    url(r'^user/profile/$', ProfileDetailView.as_view(), name='user_profile'),
    url(r'^user/profile/photo/$', ProfilePhotoView.as_view(), name='user_profile_photo'),
]