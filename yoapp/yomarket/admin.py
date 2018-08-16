from django.contrib import admin
from .models import Shop, Offer, QRcoupon, Transaction


class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'category', 'price', 'discount', 'discount_type', 'available', 'created', 'expire')
    list_filter = ('shop', 'category', 'discount_type', 'available')
    search_fields = ('title', 'description')
    date_hierarchy = 'created'
    ordering = ['created', 'available']


class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'user', 'manager', 'created')
    list_filter = ('user',)
    search_fields = ('title', 'address')
    date_hierarchy = 'created'
    ordering = ['-id', ]


class QRcouponAdmin(admin.ModelAdmin):
    list_display = ('uuid_id',  'expiry_date',  'offer')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer',  'manager',  'offer', 'points', 'created')


admin.site.register(Shop, ShopAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(QRcoupon, QRcouponAdmin)
admin.site.register(Transaction, TransactionAdmin)
