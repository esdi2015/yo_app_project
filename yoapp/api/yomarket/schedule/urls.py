from django.conf.urls import url
from .views import ScheduleListView, ScheduleDetailView

urlpatterns = [
    url(r'^schedules/$', ScheduleListView.as_view(), name='offer-list'),
    url(r'^schedules/(?P<pk>\d+)/$', ScheduleDetailView.as_view(), name='offer-detail'),
]
