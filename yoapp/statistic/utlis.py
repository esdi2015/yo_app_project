from statistic.models import StatisticTable
from yomarket.models import Offer,Shop


def count_shown(obj=None):
    if isinstance(obj, Offer):
        StatisticTable(type='shown',offer=obj).save()
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

