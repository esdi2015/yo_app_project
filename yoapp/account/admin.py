from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'rank', 'date_birth', 'photo', 'gender']
    list_filter = ('gender', )


admin.site.register(Profile, ProfileAdmin)
