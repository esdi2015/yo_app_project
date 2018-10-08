from django.contrib import admin
from targeting.models import UserPreferencesTable,UserDataTable


class TargetingAdmin(admin.ModelAdmin):
    list_display = ('data','user','object_type','object_id','created')


class TargetingUserDataAdmin(admin.ModelAdmin):
    list_display = ('birth_date','checkbox1','checkbox2')



admin.site.register(UserPreferencesTable,TargetingAdmin)
admin.site.register(UserDataTable,TargetingUserDataAdmin)

