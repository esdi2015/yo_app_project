from celery import shared_task
import celery
from django.utils import timezone
from django.db.models import Q

from notification.models import Notification_settings, Subscription, Notification
from yomarket.models import Offer
from push_notifications.models import GCMDevice



@shared_task(bind=True)
def send_notification(self,notif_id):
    notif = Notification.objects.get(id=notif_id)
    device = GCMDevice.objects.get(user=notif.user)
#   device.send_message(notif.offer.title)
    device.send_message(notif.offer.description,title = notif.offer.title, extra={"offer_id":notif.offer.id})
    notif.is_sent=True
    notif.save()

# @shared_task(bind=True)
# def subscription_task(self):
#      notif=Notification.objects.all().first()
#      send_notification.delay(notif.id)



@shared_task(bind=True)
def  subscription_task(self):
    task='api.notification.tasks.subscription_task'
    settings,created=Notification_settings.objects.get_or_create(task=task)
    lrt= settings.last_run_time

    offers=Offer.objects.filter(created__gte=lrt)
    for offer in offers:

        subs=Subscription.objects.filter(category=offer.category,type='category')
        for sub in subs:
            if sub.discount_filter == False:
                notif=Notification.objects.create(user=sub.user,offer=offer)
                send_notification.delay(notif.id)
            elif sub.discount_value <= offer.discount:
                notif=Notification.objects.create(user=sub.user,offer=offer)
                send_notification.delay(notif.id)


        subs = Subscription.objects.filter(shop=offer.shop, type='shop')
        for sub in subs:
            notif=Notification.objects.create(user=sub.user,offer=offer)
            send_notification.delay(notif.id)


    # print(timezone.now())
    # print(offers)


    settings.last_run_time=timezone.now()
    settings.save()



# @shared_task(bind=True)
# def  subscription_task(self):
#     task='api.notification.tasks.subscription_task'
#     settings,created=Notification_settings.objects.get_or_create(task=task)
#     lrt= settings.last_run_time
#
#     offers=Offer.objects.filter(created__gte=lrt)
#     for offer in offers:
#         subs=Subscription.objects.filter(Q(category=offer.category) | Q(shop=offer.shop))
#         for sub in subs:
#             Notification(user=sub.user,offer=offer).save()
#
#     print(timezone.now())
#     print(offers)
#
#
#     settings.last_run_time=timezone.now()
#     settings.save()
