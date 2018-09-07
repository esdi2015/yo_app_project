from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from yomarket.models import Shop, Offer

UserModel = get_user_model()


class StatisticTable(models.Model):
    TYPE = (
        ('redeemed', 'redeemed coupons for offer/shop'),
        ('taken', 'taken coupons for offer/shop'),
        ('liked', 'likes for offer/shop'),
        ('shown', 'views for offer/shop'),

    )

    type = models.CharField(max_length=8, choices=TYPE, default='email')
    date = models.DateTimeField(editable=True, default=timezone.now)
    value = models.IntegerField(default=1)

    offer = models.ForeignKey(Offer,on_delete=models.CASCADE,null=True,blank=True)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name = "statistic"
        verbose_name_plural = "statistics"
