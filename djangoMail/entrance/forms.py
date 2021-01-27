from .models import UsersMailing
from django.contrib import auth
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, CheckboxInput


class EntranceForm(ModelForm):
    class Meta:
        model = UsersMailing
        fields = ['login', 'password', 'remember_me']

        widgets = {
            "login": TextInput(attrs={
                'class': 'input100',
            }),
            "password": TextInput(attrs={
                'class': 'input100',
            }),
            "remember_me": CheckboxInput(attrs={
                # 'class': 'contact100-form-checkbox',
                # 'id': 'ckb1',
            }),
        }
