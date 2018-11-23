from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from yoapp.settings import DEFAULT_FROM_EMAIL

from ...views import custom_api_response
from .serializers import BusinessRequsetSerializer
from django.core.mail import send_mail
from api.utils import ERROR_API



class BusinessRequest(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BusinessRequsetSerializer
    def post(self, request, format=None):
        serializer=self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            phone=serializer.validated_data['phone']
            name=serializer.validated_data['name']

            message = "Business name: "+name+"\n"+\
                      "Phone number: "+phone+"\n"+\
                      "Email: "+email

            int_of_success = send_mail(from_email=DEFAULT_FROM_EMAIL, recipient_list=[email,],subject='YO-HALAP: New business request',message=message)
            if int_of_success == 1:
                error = {"detail": ERROR_API['500'][1]}
                error_codes = [ERROR_API['500'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_200_OK)
            else:
                error = {"detail": ERROR_API['123'][1]}
                error_codes = [ERROR_API['123'][0]]
                return Response(custom_api_response(errors=error,error_codes=error_codes),status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {"detail": ERROR_API['163'][1]}
            error_codes = [ERROR_API['163'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes),
                            status=status.HTTP_400_BAD_REQUEST)