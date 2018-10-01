from django.contrib import admin

from .models import History



class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'event', 'category', 'shop', 'offer',)
    list_filter = ('event', 'category', 'shop', 'offer', 'user', )
    search_fields = ('user__email', 'shop__title', )


admin.site.register(History, HistoryAdmin)
