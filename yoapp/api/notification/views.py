from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model

from push_notifications.models import GCMDevice
from rest_framework import status
from rest_framework.response import Response

from notification.models import Notification, Subscription
from ..views import custom_api_response
from api.notification.serializers import NotificationSerializator, SubscriptionSerializator

from common.models import Category
from yomarket.models import Shop

from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

UserModel = get_user_model()


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
    user_pk = request.data['user_pk']
    user = UserModel.objects.get(pk=user_pk)

    notif = Notification.objects.filter(user=user)

    serializer = NotificationSerializator(notif, many=True)
    return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes(())
def subscribe(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    serializer = SubscriptionSerializator(data=request.data)
    if serializer.is_valid():
        serializer.save(user_id=request.user.pk)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes(())
def unsubscribe(request, pk):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    subs = Subscription.objects.filter(pk=pk)
    subs.delete()
    return Response(custom_api_response(content={'detail': 'ok'}), status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes(())
def get_subscription(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    subs = Subscription.objects.filter(user=request.user)
    serializer = SubscriptionSerializator(subs, many=True)
    return Response(custom_api_response(serializer), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes(())
def read_notification(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    notification_id=request.data.get('notification_id')

    try:
        notification=Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        return Response(custom_api_response(metadata={'error':'wrong id or no notification'}),status.HTTP_400_BAD_REQUEST)
    notification.is_read=True
    notification.save()

    return Response(custom_api_response(metadata={'status':'ok'}), status=status.HTTP_200_OK)


