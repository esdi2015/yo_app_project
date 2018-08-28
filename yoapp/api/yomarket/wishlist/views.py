from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response


from api.views import custom_api_response

from yomarket.models import WishList
from .serializers import WishListSerializator

UserModel=get_user_model()


from django.apps import apps
from rest_framework import generics
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response



@api_view(['GET'])
@permission_classes(())
def list_like(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    wishes  =WishList.objects.filter(user=request.user)

    serializer = WishListSerializator(wishes,many=True)
    return Response(custom_api_response(serializer), status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes(())
def unlike(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    serializer = WishListSerializator(data=request.data)

    if serializer.is_valid():
        try:
             serializer.delete(user=request.user)
        except WishList.DoesNotExist:
            return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(())
def like(request):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    serializer = WishListSerializator(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
    else:
        return Response(custom_api_response(serializer), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes(())
def is_liked(request,offer_id):
    if request.user.is_authenticated == False:
        error = {"detail": "You must have to log in first"}
        return Response(custom_api_response(errors=error), status=status.HTTP_400_BAD_REQUEST)

    try:
        wishlist= WishList.objects.get(user=request.user,offer=offer_id)
    except WishList.DoesNotExist:
        return Response(custom_api_response(content={'offer':int(offer_id),'is_liked':False}),status.HTTP_200_OK)
    serializer=WishListSerializator(wishlist)
    return Response (custom_api_response(serializer),status.HTTP_200_OK)

