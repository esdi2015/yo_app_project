from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..utils import ERROR_API

from ..views import custom_api_response
from rest_framework import generics
from history.models import History
from .serializer import HistorySerializer
from django_filters.rest_framework import DjangoFilterBackend

class MyHistoryView(generics.ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('event',)

    def get_queryset(self):
        user = self.request.user
        queryset = History.objects.filter(user=user)
        return queryset

    def list(self,request, *args, **kwargs):
        queryset=self.filter_queryset(self.get_queryset())
        queryset=queryset.order_by('date').reverse()[:10]
        if queryset.exists():
            serilizer=self.get_serializer(queryset,many=True)
            return Response(custom_api_response(serilizer),status=status.HTTP_200_OK)
        error = {"detail": ERROR_API['201'][1]}
        error_codes = [ERROR_API['201'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)

