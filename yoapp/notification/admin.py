from django.contrib import admin

# Register your models here.
from django.contrib import admin
from notification.models import Notification,Subscription



class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user','offer','type','is_sent','is_read','error')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user','notification_type','type','shop','category','discount_filter','discount_value',)



admin.site.register(Notification, NotificationAdmin)
admin.site.register(Subscription,SubscriptionAdmin)