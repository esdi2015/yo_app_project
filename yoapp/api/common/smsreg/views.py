



from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


import random


from ...views import custom_api_response
from django.contrib.auth import get_user_model

UserModel = get_user_model()
from common.models import PasscodeVerify
from rest_auth.models import TokenModel


@api_view(['POST'])
def Register(request):
    if request.method == 'POST':
        try:
            mobile = request.data['mobile']
        except:
            return Response(custom_api_response(content={'error': 'invalid data'}), status=status.HTTP_400_BAD_REQUEST)

        passcode =random.randint(1000,9999)

        passcode_entry, created = PasscodeVerify.objects.update_or_create(mobile=mobile,defaults={'passcode': passcode})
        if created==False:
            passcode_entry.is_verified=False
            passcode_entry.is_sent=False
            passcode_entry.save()

        #возможно тычок в очередь целери на отправку смс/крон таск
        return Response(custom_api_response(content={"status":"ok",'passcode':passcode_entry.passcode}),status=status.HTTP_200_OK)




@api_view(['POST'])
def Verify(request):
    first_login=False

    if request.method == 'POST':
        try:
            mobile = request.data['mobile']
            passcode = request.data['passcode']
        except:
            return Response(custom_api_response(content={'error': 'invalid data'}), status=status.HTTP_400_BAD_REQUEST)

        try:
            passcode_entry = PasscodeVerify.objects.get(mobile=mobile,passcode=passcode,is_verified=False)
            user, created = UserModel.objects.update_or_create(mobile=mobile)
            token = TokenModel.objects.get(user=user)
            passcode_entry.is_verified=True
            passcode_entry.save()
        except PasscodeVerify.DoesNotExist:
            return Response(custom_api_response(content={"error":"invalid passcode or already verified"}),status=status.HTTP_200_OK)

        if created:
            first_login=True

        return Response(custom_api_response(content= {'token': token.key, 'id': user.id, 'first_login': first_login,}),status=status.HTTP_200_OK)