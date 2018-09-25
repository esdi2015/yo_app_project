from  rest_framework import serializers
from yomarket.models import SecondaryInfo

class SecondaryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SecondaryInfo
        fields = ('id','offer','title','text')

