from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_pic',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_pic',)}),
    )

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_pic']

admin.site.register(CustomUser, CustomUserAdmin)
