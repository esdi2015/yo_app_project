from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from ..views import custom_api_response
from django.utils import timezone

from api.statistic.serializers import StatisticApiSerializer,StatisticTableSerializer,StatisticApiViewsSerializer
from statistic.models import StatisticTable


from django.db.models import Sum
from django.db.models.functions import TruncMonth,TruncYear,TruncWeek,TruncDay
from django.db.models import Q

UserModel = get_user_model()




def make_dict(queryset):
    empty_dict = {}

    for key in queryset[0].keys():
        empty_dict[key] = []

    for query in queryset:
        for key, value in query.items():
            if value==None:
                empty_dict[key].append(0)
            else:
                empty_dict[key].append(value)

    return empty_dict



class CountView(generics.CreateAPIView):
    serializer_class = StatisticTableSerializer
    model = serializer_class.Meta.model
    permission_classes = ()#IsAuthenticated)


    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(custom_api_response(serializer), status.HTTP_200_OK)



class StatisticList(generics.ListAPIView):
    serializer_class = StatisticApiSerializer

    def get_queryset(self):


        queryset = StatisticTable.objects.all()

        range = self.request.query_params.get('range',None)
        subrange = self.request.query_params.get('subrange',None)

        if range is None:
            return None

        if range == 'alltime':
            if subrange is not None and isinstance(int(subrange),int):
                queryset=queryset.filter(date__year=subrange).annotate(date_field=TruncMonth('date')).values('date_field')\
                    .annotate(taken=Sum('value',filter=Q(type='taken')),redeemed=Sum('value',filter=Q(type='redeemed'))).order_by('date_field')
                return queryset
            else:
                queryset = queryset.annotate(date_field=TruncYear('date')).values('date_field')\
                    .annotate(taken=Sum('value',filter=Q(type='taken')),redeemed=Sum('value',filter=Q(type='redeemed'))).order_by('date_field')
                return queryset

        if range == 'year':
            if subrange is not None and isinstance(int(subrange),int):
                queryset = queryset.filter(date__year=timezone.now().year,date__month=subrange).annotate(date_field=TruncDay('date')).values('date_field') \
                    .annotate(taken=Sum('value', filter=Q(type='taken')),redeemed=Sum('value', filter=Q(type='redeemed'))).order_by('date_field')
                return queryset
            else:
                queryset = queryset.filter(date__year=timezone.now().year).annotate(date_field=TruncMonth('date')).values('date_field') \
                    .annotate(taken=Sum('value', filter=Q(type='taken')),redeemed=Sum('value', filter=Q(type='redeemed'))).order_by('date_field')
                return queryset

        if range == 'month':
            if subrange is not None and isinstance(int(subrange),int):
                set = queryset.filter(date__year=timezone.now().year, date__month=timezone.now().month).annotate(date_field=TruncWeek('date')).values('date_field')\
                    .annotate(taken=Sum('value', filter=Q(type='taken')),redeemed=Sum('value', filter=Q(type='redeemed'))).order_by('date_field')
                try:
                    week=set[int(subrange)-1]
                    week=week['date_field'].isocalendar()[1]
                    queryset = queryset.filter(date__year=timezone.now().year, date__month=timezone.now().month,date__week=week).annotate(date_field=TruncDay('date')).values('date_field')\
                        .annotate(taken=Sum('value', filter=Q(type='taken')),redeemed=Sum('value', filter=Q(type='redeemed'))).order_by('date_field')

                except IndexError:
                    queryset=None

                return queryset
            else:
                queryset = queryset.filter(date__year=timezone.now().year,date__month=timezone.now().month).annotate(date_field=TruncWeek('date')).values('date_field') \
                    .annotate(taken=Sum('value', filter=Q(type='taken')),redeemed=Sum('value', filter=Q(type='redeemed'))).order_by('date_field')
                return queryset

    def list(self, request, *args, **kwargs):
         queryset=self.get_queryset()

         serializer=self.get_serializer(queryset,many=True)


         return Response(custom_api_response(serializer))




class StatisticViewsList(generics.ListAPIView):
    serializer_class = StatisticApiViewsSerializer

    def get_queryset(self):


        queryset = StatisticTable.objects.all()

        range = self.request.query_params.get('range',None)
        subrange = self.request.query_params.get('subrange',None)

        if range is None:
            return None

        if range == 'alltime':
            if subrange is not None and isinstance(int(subrange),int):
                queryset=queryset.filter(date__year=subrange).annotate(date_field=TruncMonth('date')).values('date_field')\
                    .annotate(liked=Sum('value',filter=Q(type='liked')),shown=Sum('value',filter=Q(type='shown'))).order_by('date_field')
                return queryset
            else:
                queryset = queryset.annotate(date_field=TruncYear('date')).values('date_field')\
                    .annotate(liked=Sum('value',filter=Q(type='liked')),shown=Sum('value',filter=Q(type='shown'))).order_by('date_field')
                return queryset

        if range == 'year':
            if subrange is not None and isinstance(int(subrange),int):
                queryset = queryset.filter(date__year=timezone.now().year,date__month=subrange).annotate(date_field=TruncDay('date')).values('date_field') \
                    .annotate(liked=Sum('value', filter=Q(type='liked')),shown=Sum('value', filter=Q(type='shown'))).order_by('date_field')
                return queryset
            else:
                queryset = queryset.filter(date__year=timezone.now().year).annotate(date_field=TruncMonth('date')).values('date_field') \
                    .annotate(liked=Sum('value', filter=Q(type='liked')),shown=Sum('value', filter=Q(type='shown'))).order_by('date_field')
                return queryset

        if range == 'month':
            if subrange is not None and isinstance(int(subrange),int):
                set = queryset.filter(date__year=timezone.now().year, date__month=timezone.now().month).annotate(date_field=TruncWeek('date')).values('date_field')\
                    .annotate(liked=Sum('value', filter=Q(type='liked')),shown=Sum('value', filter=Q(type='shown'))).order_by('date_field')
                try:
                    week=set[int(subrange)-1]
                    week=week['date_field'].isocalendar()[1]
                    queryset = queryset.filter(date__year=timezone.now().year, date__month=timezone.now().month,date__week=week).annotate(date_field=TruncDay('date')).values('date_field')\
                        .annotate(liked=Sum('value', filter=Q(type='liked')),shown=Sum('value', filter=Q(type='shown'))).order_by('date_field')

                except IndexError:
                    queryset=None

                return queryset
            else:
                queryset = queryset.filter(date__year=timezone.now().year,date__month=timezone.now().month).annotate(date_field=TruncWeek('date')).values('date_field') \
                    .annotate(liked=Sum('value', filter=Q(type='liked')),shown=Sum('value', filter=Q(type='shown'))).order_by('date_field')
                return queryset

    def list(self, request, *args, **kwargs):
         queryset=self.get_queryset()

         serializer=self.get_serializer(queryset,many=True)


         return Response(custom_api_response(serializer))





