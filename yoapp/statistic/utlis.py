from statistic.models import StatisticTable,Statistic
from yomarket.models import Offer,Shop,Order

TYPES =(
    ('OTHER', 'Other'),
    ('GENERAL_OFFER_VIEWS','General traffic'),
    ('OFFER_PAGE_VIEWS', 'Offer page traffic'),
    ('OFFER_ADDED_TO_CART', 'Added to cart traffic'),
    ('OFFER_BOUGHT', 'Offer bought traffic'),
    ('COUPON_TAKEN', 'Taken coupons traffic'),
    ('COUPON_USED', 'Used coupons traffic'),

)



def STATISTIC_OFFERS_VIEWS(offers):
     for offer in offers:
         s = Statistic(offer=offer,shop=offer.shop,type='GENERAL_OFFER_VIEWS')
         s.save()
     return True



def STATISTIC_OFFER_PAGE_VIEWS(offer):
    s = Statistic(offer=offer, shop=offer.shop, type='OFFER_PAGE_VIEWS')
    s.save()
    return True


def STATISTIC_ADDED_TO_CART(offer):
    s = Statistic(offer=offer, shop=offer.shop, type='OFFER_ADDED_TO_CART')
    s.save()
    return True


def STATISTIC_OFFER_BOUGHT(order_products):
    for order_product in order_products:
        s = Statistic(offer=order_product.offer, shop=order_product.offer.shop, type='OFFER_BOUGHT')
        s.save()
    return True


def STATISTIC_COUPON_TAKEN(coupons):
    for coupon in coupons:
        s = Statistic(shop=coupon.shop, type='COUPON_TAKEN')
        s.save()
    return True

def COUPON_USED(coupon):
    s = Statistic(shop=coupon.shop, type='COUPON_USED')
    s.save()
    return True



def count_shown(obj=None):
    if isinstance(obj, Offer):
        StatisticTable(type='shown',offer=obj,category=obj.category).save()
        return True
    elif isinstance(obj, Shop):
        StatisticTable(type='shown',shop=obj).save()
    else:
        return False



def count_liked(obj=None):
    if isinstance(obj, Offer):
        StatisticTable(type='liked',offer=obj).save()
        return True
    else:
        return False



def count_taken_coupons(obj=None):
    if isinstance(obj, Offer):
        StatisticTable(type='taken',offer=obj).save()
        return True
    else:
        return False



def count_redeemd_coupons(obj=None):
    if isinstance(obj, Offer):
        StatisticTable(type='redeemed',offer=obj).save()
        return True
    else:
        return False

