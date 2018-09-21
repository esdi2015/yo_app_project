from history.models import History

from yomarket.models import Shop,Offer
from common.models import Category



# view event: accpet category,shop,offer instance
def history_view_event(obj=None,user=None):
    if isinstance(obj, Offer):
        History(event='offer_view',offer=obj,user=user).save()
        return True
    elif isinstance(obj, Shop):
        History(event='shop_view',shop=obj,user=user).save()
        return True
    elif  int(obj):
        History(event='category_view',category_id=obj,user=user).save()
        return True
    else:
        return False


# like event: accpet offer instance
def history_like_event(obj=None,user=None):
    if isinstance(obj, Offer):
        History(event='like',offer=obj,user=user).save()
        return True
    else:
        return False


# make coupon event: accpet offer instance
def history_make_coupon_event(obj=None,user=None):
    if isinstance(obj, Offer):
        History(event='make_coupon',offer=obj,user=user).save()
        return True
    else:
        return False


# redeem coupon event: accpet offer instance

def history_redeem_coupon_event(obj=None,user=None):
    if isinstance(obj, Offer):
        History(event='redeem_coupon',offer=obj,user=user).save()
        return True
    else:
        return False




# shop/category subscription event: accpet shop/category instance

# def history_subscription_event(obj=None,user=None):
#     if isinstance(obj, Shop):
#         History(event='shop_subscription',shop=obj,user=user).save()
#         return True
#     elif int(obj):
#         History(event='shop_subscription', category_id=obj, user=user).save()
#         return True
#     else:
#         return False