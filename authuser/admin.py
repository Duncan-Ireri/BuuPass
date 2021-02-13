from django.contrib import admin

from .forms import AuthUserCreationForm, AuthUserChangeForm
from .models import User, AuthPermissions, Role

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

class AuthCustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number', 'roles']

admin.site.register(User, AuthCustomUserAdmin)
admin.site.register(AuthPermissions)
admin.site.register(Role)