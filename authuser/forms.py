from .models import User, AuthPermissions, Role
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class AuthUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

class AuthUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields