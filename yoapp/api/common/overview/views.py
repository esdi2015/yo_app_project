from rest_framework.decorators import api_view, permission_classes
from ...views import custom_api_response
from rest_framework.response import Response
from rest_framework import status
from ...utils import ERROR_API

from yomarket.models import Offer,Shop,Transaction
from common.models import User
from statistic.models import StatisticTable


from django.db.models import Count,Sum,F

from .serializers import OverviewOwnerSerializer,OverviewManagerSerializer

@api_view(['GET'])
@permission_classes(())
def overview_view(request):
    if request.user.is_authenticated == False:
        error = {"detail": ERROR_API['115'][0]}
        error_codes = [ERROR_API['115'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)


    if request.user.role=='OWNER':

        shops=Shop.objects.filter(user=request.user)
        offers=Offer.objects.filter(shop__in=shops)
        transactions = Transaction.objects.filter(offer__in=offers).order_by('created').reverse()[:5]

        offers_statistic = StatisticTable.objects.filter(offer__in=offers,type='shown').values('offer__title').annotate(views=Sum('value')).order_by('views').reverse()[:3]
        offers_list=list(offers_statistic)

        shops_statistic = StatisticTable.objects.filter(shop__in=shops,type='shown').annotate(shop_name=F('shop__title')).values('shop_name').annotate(views=Sum('value')).order_by('views').reverse()[:3]
        shops_list=list(shops_statistic)

        managers = Shop.objects.filter(user=request.user).values('manager__email')[:3]


        total = {"offers":offers_list,"shops":shops_list,"transactions":transactions,"managers":managers}

        serializer=OverviewOwnerSerializer(total)


        return Response(custom_api_response(serializer),status=status.HTTP_200_OK)

    elif request.user.role=='MANAGER':
        shops=Shop.objects.filter(manager=request.user)
        offers=Offer.objects.filter(shop__in=shops)

        offers_statistic = StatisticTable.objects.filter(offer__in=offers,type='shown').values('offer__title').annotate(views=Sum('value')).order_by('views').reverse()[:3]
        offers_list=list(offers_statistic)

        transactions = Transaction.objects.filter(offer__in=offers,manager=request.user).order_by('created').reverse()[:5]

        total = {"offers":offers_list,"transactions":transactions}

        serializer=OverviewManagerSerializer(total)

        return Response(custom_api_response(serializer),status=status.HTTP_200_OK)


    else:

        error = {"detail": ERROR_API['116'][1]}
        error_codes = [ERROR_API['116'][0]]
        return Response(custom_api_response(errors=error, error_codes=error_codes),status=status.HTTP_400_BAD_REQUEST)

