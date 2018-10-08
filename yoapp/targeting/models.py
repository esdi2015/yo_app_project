from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


OBJECT_TYPES = (
    ('OFFER', 'Offer'),
    ('CATEGORY', 'Category')
)

class UserPreferencesTable(models.Model):
    object_type = models.CharField(max_length=50, choices=OBJECT_TYPES, default=OBJECT_TYPES[1][1])
    object_id = models.IntegerField(default=0)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    data = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)




class UserDataTable(models.Model):
    birth_date = models.DateTimeField()
    checkbox1 = models.BooleanField(default=False)
    checkbox2 = models.BooleanField(default=False)



