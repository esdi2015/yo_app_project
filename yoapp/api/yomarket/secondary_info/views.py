from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import SecondaryInfoSerializer
from yomarket.models import SecondaryInfo
from ...views import custom_api_response
from rest_framework.response import Response
from ...utils import ERROR_API
from rest_framework import status


class SecondaryInfoListCreateView(generics.ListCreateAPIView):
    serializer_class = SecondaryInfoSerializer
    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated,)



    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else:
            return [IsAuthenticated(), ]


    def get_queryset(self):
        user_id = self.request.user.pk
        queryset = SecondaryInfo.objects.filter(offer__shop__manager_id=user_id)
        return queryset

    def list(self,request, *args, **kwargs):
        if self.request.user.is_authenticated==True and self.request.user.role in ('MANAGER','OWNER') :
            queryset=self.get_queryset()
            if queryset.exists():
                serilizer=self.get_serializer(queryset,many=True)
                return Response(custom_api_response(serilizer),status=status.HTTP_200_OK)
            else:
                error = {"detail": ERROR_API['202'][1]}
                error_codes = [ERROR_API['202'][0]]
                return Response(custom_api_response(errors=error, error_codes=error_codes),
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            error = {"detail": ERROR_API['116'][1]}
            error_codes = [ERROR_API['116'][0]]
            return Response(custom_api_response(errors=error, error_codes=error_codes), status=status.HTTP_400_BAD_REQUEST)



    def create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated==True and self.request.user.role in ('MANAGER','OWNER') :
            serializer = self.get_serializer(data=request.data,many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(custom_api_response(serializer=serializer), status=status.HTTP_201_CREATED)



class SecondaryInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SecondaryInfo.objects.all()

    serializer_class = SecondaryInfoSerializer

    def get_object(self):
        if self.request.user.role in('MANAGER','OWNER'):
            instance = super(SecondaryInfoDetailView, self).get_object()
            return instance

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        else :
            return [IsAuthenticated(), ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(custom_api_response(content={"removed":True}),status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        #return Response(serializer.data)
        return Response(custom_api_response(serializer), status=status.HTTP_200_OK)
