from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from yomarket.models import Shop, Offer
from common.models import Category

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
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        verbose_name = "statistic"
        verbose_name_plural = "statistics"



TYPES =(
    ('OTHER', 'Other'),
    ('GENERAL_OFFER_VIEWS','General traffic'),
    ('OFFER_PAGE_VIEWS', 'Offer page traffic'),
    ('OFFER_ADDED_TO_CART', 'Added to cart traffic'),
    ('OFFER_BOUGHT', 'Offer bought traffic'),
    ('COUPON_TAKEN', 'Taken coupons traffic'),
    ('COUPON_USED', 'Used coupons traffic'),

)

class Statistic(models.Model):
    type = models.CharField(max_length=40,choices=TYPES,default=TYPES[0][0])
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,null=True,blank=True)
    value = models.IntegerField(default=1)
    date = models.DateTimeField(editable=True, default=timezone.now)

