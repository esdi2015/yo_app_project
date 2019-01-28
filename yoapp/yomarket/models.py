from django.db import models
from django.conf import settings
from django.apps import apps
import uuid
from notification.utils import last_coupon_redeemed_event


DISCOUNT_TYPES = (
    ('ABSOLUTE', 'ABSOLUTE'),
    ('PERCENT', 'PERCENT'),
)

CODE_TYPES = (
    ('QRCODE', 'QR code'),
    ('BARCODE', 'Barcode'),
    ('ALPHANUMCODE', 'Alphanumeric code')
)

ALPHANUM_CODE_TYPES = (
    ('WEBSITE', 'coupon redeem website'),
    ('PHONE', 'coupon redeem phone')
)

OFFER_TYPES = (
    ('REGULAR', 'Regular'),
    ('DAILY', 'Daily')
)

OFFER_STATUSES = (
    ('DRAFT', 'Draft'),
    ('REJECTED','Rejected'),
    ('PUBLISHED', 'Published')
)


class Shop(models.Model):
    user = models.ForeignKey('common.User', related_name='shops_user',
                             on_delete = models.DO_NOTHING, null=True)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey('common.User', related_name='shops_manager',
                             on_delete = models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    outer_link = models.CharField(max_length=100, null=True, blank=True)
    social_link = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='shops/%Y/%m/%d', blank=True)
    code_type = models.CharField(max_length=50, choices=CODE_TYPES, default=CODE_TYPES[0][0])
    city = models.ForeignKey('common.City', related_name='city_user',
                             on_delete = models.DO_NOTHING, null=True, blank=True)
    categories = models.ManyToManyField('common.Category', blank=True)
    schedule = models.ForeignKey('yomarket.Schedule', on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='shop_schedule')
    banner = models.ImageField(upload_to='banners/%Y/%m/%d', blank=True)
    logo = models.ImageField(upload_to='logo/%Y/%m/%d', blank=True)


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "shop"
        verbose_name_plural = "shops"
        ordering = ['-id', ]




class Schedule(models.Model):
    title = models.CharField(max_length=200)
    shop = models.ForeignKey('yomarket.Shop', on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='schedule_shop')

    mon_open = models.TimeField(blank=True, null=True)
    mon_close = models.TimeField(blank=True, null=True)

    tue_open = models.TimeField(blank=True, null=True)
    tue_close = models.TimeField(blank=True, null=True)

    wed_open = models.TimeField(blank=True, null=True)
    wed_close = models.TimeField(blank=True, null=True)

    thu_open = models.TimeField(blank=True, null=True)
    thu_close = models.TimeField(blank=True, null=True)

    fri_open = models.TimeField(blank=True, null=True)
    fri_close = models.TimeField(blank=True, null=True)

    sat_open = models.TimeField(blank=True, null=True)
    sat_close = models.TimeField(blank=True, null=True)

    sun_open = models.TimeField(blank=True, null=True)
    sun_close = models.TimeField(blank=True, null=True)

    comment = models.TextField(blank=True)


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "schedule"
        verbose_name_plural = "schedules"




class Offer(models.Model):
    category = models.ForeignKey('common.Category', related_name='offers_from_category',
                                 on_delete=models.SET_NULL, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
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
    redeemed_codes_count = models.SmallIntegerField(('redeemed count'), default=0, editable=True)
    expire = models.DateTimeField(('expire date'), blank=False, null=False)
    coupon_description = models.CharField(max_length=300, blank=True)
    alpha_num_code_type = models.CharField(max_length=50, choices=ALPHANUM_CODE_TYPES, default=ALPHANUM_CODE_TYPES[0][0])
    coupon_phone = models.CharField(max_length=20, null=True, blank=True)
    coupon_web  = models.CharField(max_length=100, null=True, blank=True)
    code_type = models.CharField(max_length=50, choices=CODE_TYPES, default=CODE_TYPES[0][0])
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPES, default=OFFER_TYPES[0][0])
    status = models.CharField(max_length=50, choices=OFFER_STATUSES, default=OFFER_STATUSES[0][0])


    def redeemed_codes_increment(self,user=None):
        if self.redeemed_codes_count+1 == self.codes_count:
            self.redeemed_codes_count=self.redeemed_codes_count+1
            self.save()
            self.available = False
            last_coupon_redeemed_event(offer=self,user=user)
            self.save()
            coupons = QRcoupon.objects.filter(offer=self)
            for coupon in coupons:
                coupon.is_expired = True
                coupon.save()
        elif self.redeemed_codes_count < self.codes_count:
             self.redeemed_codes_count = self.redeemed_codes_count + 1
             self.save()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Transaction(models.Model):
    customer = models.ForeignKey('common.User', related_name='transactions_customer', on_delete=models.CASCADE)
    manager = models.ForeignKey('common.User', related_name='transactions_manager', on_delete=models.CASCADE)
    offer = models.ForeignKey('yomarket.Offer', related_name='transactions_offer', on_delete=models.CASCADE)
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
    is_expired = models.BooleanField(default=False)
    expiry_date = models.DateTimeField()
    date_created = models.DateTimeField(('date created'), auto_now_add=True)
    user = models.ForeignKey('common.User', related_name='coupon_user', on_delete=models.CASCADE,default=None)
    offer = models.ForeignKey(Offer, related_name='offer', on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=50, choices=CODE_TYPES, default=CODE_TYPES[0][0])
    alpha_num_code_type = models.CharField(max_length=50, choices=ALPHANUM_CODE_TYPES, default=ALPHANUM_CODE_TYPES[0][0], blank=True, null=True)
    coupon_phone = models.CharField(max_length=20, null=True, blank=True)
    coupon_web = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=300, blank=True)


    class Meta:
        verbose_name = "QRcoupon"
        verbose_name_plural = "QRcoupons"

    def __str__(self):
        return 'QRcoupon {}'.format(self.uuid_id)


class WishList(models.Model):
    user = models.ForeignKey('common.User', related_name='wish_user', on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    is_liked = models.BooleanField(default=True)

    class Meta:
        unique_together = (("user", "offer"),)


class SecondaryInfo(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)


class CardHolder(models.Model):
    user = models.ForeignKey('common.User', related_name='card_user', on_delete=models.CASCADE)
    tranzila_tk = models.CharField(max_length=30,blank=False,null=False)
    exp_date = models.DateField(blank=False,null=False)



class CartProduct(models.Model):
    user=models.ForeignKey('common.User', related_name='cart_for_user', on_delete=models.CASCADE,null=True)
    offer = models.ForeignKey(Offer,related_name='product_offer',on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_to_cart = models.DateTimeField(auto_now=True)



ORDER_STATUSES = (
    ('PAID', 'Paid'),
    ('APPROVED','Approved'),
    ('SHIPPED', 'Shipped'),
    ('DELIVERED', 'Delivered'),
    ('CANCELED', 'Canceled'),

)


class Order(models.Model):
    shop = models.ForeignKey(Shop, related_name='order_shop', on_delete=models.CASCADE)
    user = models.ForeignKey('common.User', related_name='order_for_user', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    total_sum = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=50, choices=ORDER_STATUSES)
    phone = models.CharField(max_length=30, blank=True, null=True)
    fullname = models.CharField(max_length=150, blank=True, null=True)
    coupon = models.ForeignKey('yomarket.Coupon', related_name='order_coupon',blank=True,null=True,on_delete=models.DO_NOTHING)


class OrderProduct(models.Model):
    offer = models.ForeignKey(Offer,related_name='offer_for_order_product',on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order,related_name='order_product',on_delete=models.CASCADE)


DISCOUNT_TYPES = (
    ('ABSOLUTE', 'ABSOLUTE'),
    ('PERCENT', 'PERCENT'),
)


class CouponSetting(models.Model):
    coupons_per_user = models.IntegerField(default=1)
    discount_type = models.CharField(choices=DISCOUNT_TYPES, default=DISCOUNT_TYPES[0][0],max_length=30)
    discount = models.IntegerField(default=0)
    rank = models.IntegerField(default=1)
    shop = models.ForeignKey(Shop,related_name='coupon_setting',on_delete=models.CASCADE)


COUPON_STATUSES = (
    ('AVAILABLE', 'Available'),
    ('USED', 'Used'),
    ('EXPIRED', 'Expired'),
)

class Coupon(models.Model):
    discount_type = models.CharField(choices=DISCOUNT_TYPES, default=DISCOUNT_TYPES[0][0],max_length=30)
    discount = models.IntegerField(default=0)
    user = models.ForeignKey('common.User',related_name='user_coupons',on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,related_name='coupons',on_delete=models.CASCADE)
    status = models.CharField(choices=COUPON_STATUSES,default=COUPON_STATUSES[0][0],max_length=30)
    order = models.ForeignKey(Order,related_name='order_coupon',blank=True,on_delete=models.DO_NOTHING,null=True)
    created = models.DateTimeField(auto_now_add=True)
    used = models.DateTimeField(blank=True,null=True)
    setting = models.ForeignKey(CouponSetting,on_delete=models.CASCADE,related_name='setting',null=True)


