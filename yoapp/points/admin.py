from django.contrib import admin

from .models import Point



class PointAdmin(admin.ModelAdmin):
    list_display = ('date','points','event_type','type','user', 'offer','shop')


admin.site.register(Point, PointAdmin)
