from django.contrib import admin
from .models import Profile, UserSimPackage


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'rank', 'date_birth', 'age', 'photo', 'gender']
    list_filter = ('gender', )


admin.site.register(Profile, ProfileAdmin)

admin.site.register(UserSimPackage)