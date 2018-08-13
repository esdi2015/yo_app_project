from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from yomarket.models import QRcoupon
from api.yomarket.qrcode.serializers import QRcouponSerializator
from rest_framework import status
from yomarket.models import Offer

from ...views import custom_api_response

from django.utils import timezone


@api_view(['GET'])
@permission_classes([AllowAny])
def qr_check(request, uuid):
    code = QRcoupon.objects.filter(uuid_id=uuid).first()
    if code!=None:
        serializer = QRcouponSerializator(code)
        serializer.validate_expiry_date(value=code.expiry_date)
        code.save()
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
    else:
        return Response({'code':uuid,'error':'code not found'},status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def qr_checkout(request,uuid):
    code = QRcoupon.objects.filter(uuid_id=uuid,in_transaction=True).first()
    if code!=None:
        code.in_transaction=False
        code.is_redeemed=True
        code.save()
        return Response({'code':code.uuid_id,'redeemed':True},status=status.HTTP_200_OK)
    else:
        return Response({'error':'no available code in transaction'},status.HTTP_400_BAD_REQUEST)

    offer = Offer.objects.get(pk=offer_id)
    for x in range(int(quantity)):
        code = QRcoupon(expiry_date=offer.expire,offer=offer)
        code.save()
    return Response({"quantity":quantity,"created":True}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_qrs(request):
    quantity = request.data['quantity']
    offer_id = request.data['offer_id']

    offer = Offer.objects.get(pk=offer_id)
    for x in range(int(quantity)):
        code = QRcoupon(expiry_date=offer.expire,offer=offer)
        code.save()
    return Response({"quantity":quantity,"created":True}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_code(request):
    offer_id = request.data['offer_id']
    offer = Offer.objects.get(pk=offer_id)
    code=QRcoupon.objects.filter(is_redeemed=False,in_transaction=False,offer=offer).first()
    if code!=None:
        code.in_transaction=True
        code.transaction_start_time=timezone.now()
        code.save()
        return Response({'code':code.uuid_id},status.HTTP_200_OK)
    else:
        return Response({'error':'no available codes'},status.HTTP_400_BAD_REQUEST)
