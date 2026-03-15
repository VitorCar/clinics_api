from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUsuario


class CustomUsuarioCreationForm(UserCreationForm):

    class Meta:
        model = CustomUsuario
        fields = (
            'email',
            'full_name',
            'role',
            'is_staff',
            'is_active'
        )


class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsuario
        fields = (
            'email',
            'full_name',
            'role',
            'is_active',
            'is_staff',
            'is_superuser'
        )
