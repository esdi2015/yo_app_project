from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Shop, Offer, QRcoupon, Transaction, WishList, Schedule, SecondaryInfo, CardHolder, CartProduct
from common.models import User
from yoapp.utils import ExportCsvMixin


class SecondaryInfoInline(admin.StackedInline):
    model = SecondaryInfo


class OfferAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('title', 'shop', 'category', 'price', 'discount', 'discount_type', 'available', 'created', 'expire', 'offer_type')
    list_filter = ('shop', 'category', 'discount_type', 'available', 'offer_type')
    search_fields = ('title', 'description')
    date_hierarchy = 'created'
    ordering = ['created', 'available']
    inlines = [SecondaryInfoInline]
    actions = ['export_as_csv']

    def has_add_permission(self, request, obj=None):
        return True


class ScheduleInline(admin.StackedInline):
    model = Schedule


class ShopAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('title', 'address', 'city', 'user', 'manager', 'created', 'code_type', 'categories_display')
    list_filter = ('city', 'user', 'code_type', )
    search_fields = ('title', 'address')
    date_hierarchy = 'created'
    ordering = ['-id', ]
    inlines = [ScheduleInline]
    actions = ['export_as_csv']

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
        return True

    def categories_display(self, obj):
        return ", ".join([
            category.category_name for category in obj.categories.all()
        ])

    categories_display.short_description = "Categories"


class QRcouponAdmin(admin.ModelAdmin):
    list_display = ('id','uuid_id','type','user','offer','expiry_date','is_redeemed','is_expired','date_created')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer',  'manager',  'offer', 'points', 'created')


class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'offer', 'is_liked')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'comment')
    list_filter = ('shop', )

class SecondaryInfoAdmin(admin.ModelAdmin):
    list_display = ('offer', 'title', 'text')

class CardHolderAdmin(admin.ModelAdmin):
    list_display = ('user',  'tranzila_tk',  'exp_date')



admin.site.register(Shop, ShopAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(QRcoupon, QRcouponAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(SecondaryInfo,SecondaryInfoAdmin)
admin.site.register(CardHolder,CardHolderAdmin)
admin.site.register(CartProduct)