from django.db import models
from django.contrib.auth import get_user_model

from common.models import Category
from yomarket.models import Shop,Offer

UserModel=get_user_model()


class Notification_settings(models.Model):
    task = models.CharField(max_length=150,blank=True,null=True)
    last_run_time = models.DateTimeField(blank=True,null=True)

    class Meta:
        verbose_name = "notif_settings"


class Notification(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=200)
    is_data = models.BooleanField(default=True)
    user = models.ForeignKey(UserModel, related_name='user', on_delete=models.CASCADE, null=True)
    offer = models.ForeignKey(Offer,on_delete=models.CASCADE,null=True,blank=True)
    is_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "notification"


class Subscription(models.Model):
    TYPE = (
        ('category','Category'),
        ('shop','Shop')
    )

    type = models.CharField(max_length=8,choices=TYPE)
    user = models.ForeignKey(UserModel, related_name='subscription_user', on_delete=models.CASCADE)

    category = models.ForeignKey(Category,related_name='category',on_delete=models.CASCADE,null=True,blank=True)
    shop = models.ForeignKey(Shop,related_name='subscription_shop',on_delete=models.CASCADE,null=True,blank=True)

    discount_filter = models.BooleanField(default=False,blank=True)
    discount_value = models.IntegerField(default=0,blank=True)

    def __str__(self):
        return (self.type+" "+self.user.email)

    class Meta:
        verbose_name = "subscription"

