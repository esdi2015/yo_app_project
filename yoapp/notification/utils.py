from django.template.loader import render_to_string
from django.apps import apps

def make_email_msg(notification,request=None):
   if notification.message_type=='new_offer':
        html_message = render_to_string(request=request,template_name='new_offer.html', context={"offer": notification.offer})
        subject = 'HALAP New Offer available: '+notification.offer.title
        message = html_message
        answer= {"html_message":html_message,'subject':subject,'message':message}
        return answer
   elif notification.message_type=='last_coupon_redeemed':
        html_message = render_to_string(request=request, template_name='last_coupon_redeemed.html', context={"offer": notification.offer})
        subject = 'HALAP Sorry, last coupon was redeemed: ' + notification.offer.title
        message = html_message
        answer = {"html_message": html_message, 'subject': subject, 'message': message}
        return answer
   elif notification.message_type=='few_coupons_left':
        html_message = render_to_string(request=request, template_name='few_coupons_left.html', context={"offer": notification.offer})
        subject = 'HALAP Hurry up,only 20% of coupons remain: ' + notification.offer.title
        message = html_message
        answer = {"html_message": html_message, 'subject': subject, 'message': message}
        return answer
   else:
       return False


def make_push_msg(notification):
    if notification.message_type == 'new_offer':
        return {'extra':{"offer_id":notification.offer.id},
                'title':'New offer is available:',
                'message': notification.offer.title }
    if notification.message_type == 'last_coupon_redeemed':
        return {'data':{'extra':{"offer_id":notification.offer.id},
                'title':'Sorry, last coupoun was redeemed:',
                'message': notification.offer.title }}
    if notification.message_type == 'few_coupons_left':
        return {'data':{'extra':{"offer_id":notification.offer.id},
                'title':'Hurry, only 20% of coupons left:',
                'message': notification.offer.title
                }}


def last_coupon_redeemed_event(offer=None,user=None):
     Notification = apps.get_model('notification', 'Notification')

     if user.profile.notifications == 'enabled':
         notif = Notification.objects.create(user=user, offer=offer, type='email', title=offer.title,
                                             body=offer.description, message_type="last_coupon_redeemed")
         notif = Notification.objects.create(user=user, offer=offer, type='push', title=offer.title,
                                             body=offer.description, message_type="last_coupon_redeemed")

     if user.profile.notifications == 'push':
         notif = Notification.objects.create(user=user, offer=offer, type='push', title=offer.title,
                                             body=offer.description, message_type="last_coupon_redeemed")

     if user.profile.notifications == 'email':
         notif = Notification.objects.create(user=user, offer=offer, type='email', title=offer.title,
                                             body=offer.description, message_type="last_coupon_redeemed")

