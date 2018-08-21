
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model

from push_notifications.models import GCMDevice
from rest_framework import status
from rest_framework.response import Response


from notification.models import Notification,Subscription
from ..views import custom_api_response
from api.notification.serializers import NotificationSerializator

from common.models import Category
from yomarket.models import Shop

UserModel=get_user_model()


from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

@api_view(['POST'])
@permission_classes(())
def test_func(request):
    subs=Subscription.objects.filter(type='category')
    for sub in subs:
        user = sub.user
        pass


@api_view(['POST'])
@permission_classes(())
def get_notifications(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)
    user_pk=request.data['user_pk']
    user=UserModel.objects.get(pk=user_pk)

    notif=Notification.objects.filter(user=user)

    serializer = NotificationSerializator(notif,many=True)
    return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes(())
def subscribe(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    user=request.user
    type = request.data.get('type')
    shop = Shop.objects.filter(id=request.data.get('shop_id')).first()
    category = Category.objects.filter(category_name=request.data.get('category_name')).first()
    discount_filter = request.data.get('discount_filter')
    discount_value = request.data.get('discount_value')

    sub = Subscription(user=request.user,type=type,shop=shop,category=category,discount_filter=discount_filter,discount_value=discount_value)
    sub.save()

    return Response('ok', status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes(())
def unsubscribe(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    type = request.data.get('type')
    shop_id = request.data.get('shop_id')
    category_name = request.data.get('category_name')
    if type == 'category':
        category=Category.objects.get(category_name=category_name)
        sub=Subscription.objects.filter(type=type,category=category)
        sub.delete()
        return Response('ok', status=status.HTTP_200_OK)

    elif type =='shop':
        shop=Shop.objects.get(id=shop_id)
        sub = Subscription.objects.filter(type=type, shop=shop)
        sub.delete()
        return Response('ok', status=status.HTTP_200_OK)
    return Response({'error':'wrong data'}, status=status.HTTP_400_BAD_REQUEST)


