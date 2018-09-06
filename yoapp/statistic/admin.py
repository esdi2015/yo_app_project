from django.contrib import admin
from statistic.models import StatisticTable


class StatisticAdmin(admin.ModelAdmin):
    list_display = ('offer','type','value','date')


admin.site.register(StatisticTable, StatisticAdmin)
