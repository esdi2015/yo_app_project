from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Shop, Offer, QRcoupon, Transaction, WishList
from common.models import User


class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'category', 'price', 'discount', 'discount_type', 'available', 'created', 'expire', 'offer_type')
    list_filter = ('shop', 'category', 'discount_type', 'available', 'offer_type')
    search_fields = ('title', 'description')
    date_hierarchy = 'created'
    ordering = ['created', 'available']


class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'user', 'manager', 'created', 'code_type')
    list_filter = ('user', 'code_type')
    search_fields = ('title', 'address')
    date_hierarchy = 'created'
    ordering = ['-id', ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role="OWNER")
        elif db_field.name == "manager":
            kwargs["queryset"] = User.objects.filter(role="MANAGER")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class QRcouponAdmin(admin.ModelAdmin):
    list_display = ('uuid_id',  'expiry_date',  'offer')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer',  'manager',  'offer', 'points', 'created')


class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'offer', 'is_liked')


admin.site.register(Shop, ShopAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(QRcoupon, QRcouponAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(WishList, WishListAdmin)
