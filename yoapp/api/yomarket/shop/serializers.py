from django.apps import apps
from rest_framework import serializers


ShopModel = apps.get_model('yomarket', 'Shop')


class ShopSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(allow_null=False)

    class Meta:
        model = ShopModel
        fields = ('id', 'title', 'address', 'user', 'user_id')

    # def to_representation(self, instance):
    #     # instance is the model object. create the custom json format by accessing instance attributes normaly
    #     # and return it
    #     identifiers = dict()
    #     identifiers['id'] = instance.id
    #     identifiers['title'] = instance.title
    #
    #     representation = {
    #         'identifiers': identifiers,
    #         #'user_id': instance.user_id,
    #         'address': instance.address
    #     }
    #
    #     return representation