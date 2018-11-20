from rest_framework import serializers

class BusinessRequsetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200,allow_blank=True)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=100)