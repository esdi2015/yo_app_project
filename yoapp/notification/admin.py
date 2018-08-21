from django.contrib import admin

# Register your models here.
from django.contrib import admin
from notification.models import Notification,Subscription



class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title',  'body',  'is_data','user')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user','type','shop','category','discount_filter','discount_value')



admin.site.register(Notification, NotificationAdmin)
admin.site.register(Subscription,SubscriptionAdmin)