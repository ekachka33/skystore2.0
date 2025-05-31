# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # Импортируем стандартный UserAdmin
from .models import User # Импортируем нашу кастомную модель User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone_number', 'country', 'is_staff', 'is_active', 'is_superuser')

    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')

    search_fields = ('email', 'phone_number', 'country')

    list_editable = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('avatar', 'phone_number', 'country')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'),
        }),
    )

    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)