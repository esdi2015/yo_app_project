from django.contrib import admin
from targeting.models import UserPreferencesTable


class TargetingAdmin(admin.ModelAdmin):
    list_display = ('data','user','object_type','object_id','created')


admin.site.register(UserPreferencesTable,TargetingAdmin)
