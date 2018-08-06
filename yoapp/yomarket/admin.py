from django.contrib import admin
from .models import Shop, Offer


class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'category', 'price', 'discount', 'discount_type', 'available', 'created')
    list_filter = ('shop', 'category', 'discount_type', 'available')
    search_fields = ('title', 'description')
    date_hierarchy = 'created'
    ordering = ['created', 'available']


admin.site.register(Shop)
admin.site.register(Offer, OfferAdmin)
