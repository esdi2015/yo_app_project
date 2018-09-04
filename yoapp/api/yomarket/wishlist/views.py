from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response


from api.views import custom_api_response

from yomarket.models import WishList
from .serializers import WishListSerializator,WishListNestedSerializator

UserModel=get_user_model()


from django.apps import apps
from rest_framework import generics
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError


class MyCouponsListView(generics.ListAPIView):
    serializer_class = WishListNestedSerializator
    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.pk
        queryset = self.model.objects.filter(user_id=user_id)
        return queryset

    def list(self,request, *args, **kwargs):
        queryset=self.get_queryset()
        if queryset.exists():
            serilizer=self.get_serializer(queryset,many=True)
            return Response(custom_api_response(serilizer),status=status.HTTP_200_OK)
        return Response(custom_api_response(content={'error':'no coupons'}),status.HTTP_400_BAD_REQUEST)




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



class LikeView(generics.CreateAPIView):
    serializer_class = WishListSerializator
    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated,)


    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            return Response(custom_api_response(serializer), status.HTTP_200_OK)
        except IntegrityError:
            return Response(custom_api_response(content={'is_liked':True}),status.HTTP_200_OK)





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

