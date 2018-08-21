from django.db import models
from django.conf import settings
from django.apps import apps

import uuid


DISCOUNT_TYPES = (
    ('ABSOLUTE', 'ABSOLUTE'),
    ('PERCENT', 'PERCENT'),
)


class Shop(models.Model):
    user = models.ForeignKey('common.User', related_name='shops_user',
                             on_delete = models.DO_NOTHING)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey('common.User', related_name='shops_manager',
                             on_delete = models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    outer_link = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='shops/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.title

    # def __unicode__(self):
    #     return self.title


class Offer(models.Model):
    category = models.ForeignKey('common.Category', related_name='offers_from_category',
                                 on_delete=models.DO_NOTHING)
    shop = models.ForeignKey(Shop, related_name='shop_offer', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='offers/%Y/%m/%d', blank=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(max_length=50, choices=DISCOUNT_TYPES, default='ABSOLUTE')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code_data = models.CharField(max_length=200, blank=True)
    codes_count = models.SmallIntegerField(('codes count'), default=0, editable=True)
    expire = models.DateTimeField(('expire date'), blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    customer = models.ForeignKey('common.User', related_name='transactions_customer', on_delete=models.DO_NOTHING)
    manager = models.ForeignKey('common.User', related_name='transactions_manager', on_delete=models.DO_NOTHING)
    offer = models.ForeignKey('yomarket.Offer', related_name='transactions_offer', on_delete=models.DO_NOTHING)
    points = models.IntegerField(default=0, editable=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return 'Gets {}'.format(self.points)


class QRcoupon(models.Model):
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    is_redeemed = models.BooleanField(default=False)
    in_transaction = models.BooleanField(default=False)
    expiry_date = models.DateTimeField()
    transaction_start_time= models.DateTimeField(null=True)
    date_created = models.DateTimeField(('date created'), auto_now_add=True)
    offer = models.ForeignKey(Offer, related_name='offer', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "QRcoupon"
        verbose_name_plural = "QRcoupons"

    def __str__(self):
        return 'QRcoupon {}'.format(self.uuid_id)
