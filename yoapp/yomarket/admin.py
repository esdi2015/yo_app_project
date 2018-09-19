from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Shop, Offer, QRcoupon, Transaction, WishList, Schedule
from common.models import User


class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'category', 'price', 'discount', 'discount_type', 'available', 'created', 'expire', 'offer_type')
    list_filter = ('shop', 'category', 'discount_type', 'available', 'offer_type')
    search_fields = ('title', 'description')
    date_hierarchy = 'created'
    ordering = ['created', 'available']

    def has_add_permission(self, request, obj=None):
        return False


class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'city', 'user', 'manager', 'created', 'code_type')
    list_filter = ('city', 'user', 'code_type', )
    search_fields = ('title', 'address')
    date_hierarchy = 'created'
    ordering = ['-id', ]

    shop_id_for_formfield = None

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.shop_id_for_formfield = obj.id
        return super(ShopAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role="OWNER")
        elif db_field.name == "manager":
            kwargs["queryset"] = User.objects.filter(role="MANAGER")
        elif db_field.name == "schedule":
            kwargs["queryset"] = Schedule.objects.filter(shop_id=self.shop_id_for_formfield)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request, obj=None):
        return False


class QRcouponAdmin(admin.ModelAdmin):
    list_display = ('id','uuid_id','type','user','offer','expiry_date','is_redeemed','is_expired')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer',  'manager',  'offer', 'points', 'created')


class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'offer', 'is_liked')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'comment')
    list_filter = ('shop', )


admin.site.register(Shop, ShopAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(QRcoupon, QRcouponAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Schedule, ScheduleAdmin)
