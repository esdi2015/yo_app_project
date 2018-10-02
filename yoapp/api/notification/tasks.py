from celery import shared_task
import celery
from django.utils import timezone
from django.db.models import Q
from django.core.mail import send_mail
from yoapp.settings import DEFAULT_FROM_EMAIL

from notification.models import Notification_settings, Subscription, Notification
from yomarket.models import Offer,QRcoupon
from push_notifications.models import GCMDevice
from notification.utils import make_email_msg,make_push_msg


@shared_task(bind=True,ignore_result=True)
def send_notification(self,notif_id):
    notif = Notification.objects.get(id=notif_id)
    if notif.type == 'push':
        try:
            device = GCMDevice.objects.get(user=notif.user)
            answer = make_push_msg(notif)
            device.send_message(**answer)
            notif.is_sent = True
            notif.save()
        except GCMDevice.DoesNotExist:
            notif.error="no device"
            notif.save()
    elif notif.type == 'email':
        answer=make_email_msg(notif)
        int_of_success = send_mail(from_email=DEFAULT_FROM_EMAIL,recipient_list=[notif.user.email], **answer)
        if int_of_success == 1:
            notif.is_sent=True
            notif.save()
        else:
            notif.error = "email error"
            notif.save()


# @shared_task(bind=True)
# def subscription_task(self):
#      notif=Notification.objects.all().first()
#      send_notification.delay(notif.id)



@shared_task(bind=True,ignore_result=True)
def subscription_task(self):
    task='api.notification.tasks.subscription_task'
    settings,created=Notification_settings.objects.get_or_create(task=task)
    if created==True:
        settings.last_run_time = timezone.now()
        settings.save()
    lrt= settings.last_run_time

    offers=Offer.objects.filter(created__gte=lrt)
    for offer in offers:

        subs=Subscription.objects.filter(category=offer.category,type='category')
        for sub in subs:
            if sub.discount_filter == False:
                notif=Notification.objects.create(user=sub.user,offer=offer,type=sub.notification_type,title=offer.title,body=offer.description,message_type="new_offer")
                send_notification.delay(notif.id)
            elif sub.discount_value <= offer.discount:
                notif=Notification.objects.create(user=sub.user,offer=offer,type=sub.notification_type,title=offer.title,body=offer.description,message_type="new_offer")
                send_notification.delay(notif.id)


        subs = Subscription.objects.filter(shop=offer.shop, type='shop')
        for sub in subs:
            notif=Notification.objects.create(user=sub.user,offer=offer,type=sub.notification_type,title=offer.title,body=offer.description,message_type="new_offer")
            send_notification.delay(notif.id)


    settings.last_run_time=timezone.now()
    settings.save()





@shared_task(bind=True,ignore_result=True)
def last_coupon_redeemed_task(self):
    task='api.notification.tasks.last_coupon_redeemed_task'
    settings,created=Notification_settings.objects.get_or_create(task=task)
    if created==True:
        settings.last_run_time = timezone.now()
        settings.save()
    lrt= settings.last_run_time

    notifs = Notification.objects.all().filter(message_type='last_coupon_redeemed',is_sent=False,is_read=False)

    for notif in notifs:
        send_notification.delay(notif.id)

    settings.last_run_time=timezone.now()
    settings.save()



@shared_task(bind=True,ignore_result=True)
def coupon_balance_task(self):
    task='api.notification.tasks.coupon_balance_task'
    settings,created=Notification_settings.objects.get_or_create(task=task)
    if created==True:
        settings.last_run_time = timezone.now()
        settings.save()
    lrt= settings.last_run_time

    offers=Offer.objects.filter(available=True).exclude(id__in =settings.list)

    for offer in offers:
        percent=(offer.redeemed_codes_count/offer.codes_count)*100

        if percent>=80:
            coupons_users = QRcoupon.objects.filter(offer=offer,is_redeemed=False,is_expired=False).values_list('user',flat=True)
            for user_id in coupons_users:
                notif=Notification(user_id=user_id,offer=offer,title=offer.title,body=offer.description,type='email',message_type='few_coupons_left')
                notif.save()
                send_notification.delay(notif.id)

            settings.list.append(offer.pk)


    settings.last_run_time=timezone.now()
    settings.save()

