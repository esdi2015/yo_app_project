from celery import shared_task
from django.utils import timezone
from django.db.models import DateTimeField, ExpressionWrapper, F
from notification.models import Notification_settings, Subscription, Notification
from yomarket.models import QRcoupon




@shared_task(bind=True,ignore_result=True)
def coupon_ttl_task(self):
    task='api.notification.tasks.coupon_ttl_task'
    settings,created=Notification_settings.objects.get_or_create(task=task)
    if created==True:
        settings.last_run_time = timezone.now()
        settings.save()
    lrt= settings.last_run_time

    coupons = QRcoupon.objects.filter(is_redeemed=False,is_expired=False)\
        .annotate(created=ExpressionWrapper(F('date_created') + timezone.timedelta(seconds=900), output_field=DateTimeField()))\
        .filter(created__lte=timezone.now())



    for coupon in coupons:
        coupon.delete()

    settings.last_run_time=timezone.now()
    settings.save()




