from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Team, Membership
from .forms import CustomUserCreate, CustomUserChange

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreate
    form = CustomUserChange
    model = CustomUser
    list_display = ('nome_completo', 'email', 'interesse', 'linkedin', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Info', {'fields': ('nome_completo', 'interesse', 'linkedin')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'focus', 'max', 'description', 'private')

