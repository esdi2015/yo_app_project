from django.apps import apps
from rest_framework import serializers
from history.models import History


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = ('user', 'date', 'event', 'category', 'shop','offer','search_text')



