# from celery import shared_task
#
# from notification.models import Subscription
#
#
#
# @shared_task(rate_limit='1/m')
# def subscription_category_task():
#     subs = Subscription.objects.filter(type='category')
#     pass