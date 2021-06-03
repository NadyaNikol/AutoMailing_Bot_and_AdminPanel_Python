from .models import UsersMailing
from django.forms import ModelForm, TextInput, CheckboxInput, PasswordInput


class EntranceForm(ModelForm):
    class Meta:
        model = UsersMailing
        fields = ['login', 'password', 'remember_me']

        widgets = {
            "login": TextInput(attrs={
                'class': 'message_input',
            }),
            "password": PasswordInput(attrs={

                'render_value': True,
                'class': 'message_input'
            }),
            "remember_me": CheckboxInput(attrs={
                # 'class': 'contact100-form-checkbox',
                # 'id': 'ckb1',
            }),
        }
