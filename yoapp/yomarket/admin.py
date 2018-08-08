from django.contrib import admin
from .models import Shop, Offer


class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'category', 'price', 'discount', 'discount_type', 'available', 'created', 'expire')
    list_filter = ('shop', 'category', 'discount_type', 'available')
    search_fields = ('title', 'description')
    date_hierarchy = 'created'
    ordering = ['created', 'available']


class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'user', 'created')
    list_filter = ('user',)
    search_fields = ('title', 'address')
    date_hierarchy = 'created'
    ordering = ['-id', ]


admin.site.register(Shop, ShopAdmin)
admin.site.register(Offer, OfferAdmin)
