from django.contrib import admin
from .models import UserFollow


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('user__username', 'followed_user__username')


# Register your models here.
