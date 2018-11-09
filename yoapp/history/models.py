from django.db import models
from common.models import User, Category
from yomarket.models import Offer, Shop


EVENT_TYPES = (
    ('else','Else actions'),
    ('offer_view', 'View offer'),
    ('shop_view', 'View shop'),
    ('category_view', 'View category'),
    ('like', 'Liked offer'),
    ('make_coupon', 'Maked coupon'),
    ('redeem_coupon', 'Redeemed coupon'),
    ('shop_subscription','Subscribed to shop'),
    ('category_subscription', 'Subscribed to category'),
    ('profile_update', 'Profile updated'),
    ('offer_search', 'Offer search'),
    ('shop_search', 'Shop search'),

)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=False,null=False)
    event = models.CharField(max_length=100,choices=EVENT_TYPES,default=EVENT_TYPES[0][0])
    date = models.DateTimeField(auto_now_add=True)
    search_text = models.CharField(max_length=300,null=True,blank=True)

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE,blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True)

