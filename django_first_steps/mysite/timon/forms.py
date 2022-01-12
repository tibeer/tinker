from django.forms import ModelForm, PasswordInput
# flake8: noqa
from .models import *


class ProviderCreateForm(ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'username', 'password']
        widgets = {'password': PasswordInput(),}


class ProviderUpdateForm(ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'username', 'password']
        widgets = {'password': PasswordInput(),}