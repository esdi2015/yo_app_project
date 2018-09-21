from django.contrib import admin

from .models import History



class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user','date','event','category','shop', 'offer',)


admin.site.register(History, HistoryAdmin)
