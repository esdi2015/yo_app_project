from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_birth', 'photo', 'gender']


admin.site.register(Profile, ProfileAdmin)
