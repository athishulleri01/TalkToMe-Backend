from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role','is_active', 'is_otp_verify')
    list_display_links = ('username',)

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Extra Details',
            {
                'fields': (
                    'phone_number',
                    'profile_picture',
                    'is_blocked',
                    'role',
                    'is_paid',
                    'country'

                ),
            }
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
