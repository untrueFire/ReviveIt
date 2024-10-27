from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Item, Transaction

User = get_user_model()


class MyUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (("余额", {"fields": ("balance",)}),)


admin.site.register(User, MyUserAdmin)
admin.site.register(Item)
admin.site.register(Transaction)
