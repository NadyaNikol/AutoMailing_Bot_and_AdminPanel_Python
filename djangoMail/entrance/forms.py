from .models import UsersMailing
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea


class EntranceForm(ModelForm):
    class Meta:
        model = UsersMailing
        fields = ['login', 'password']

        widgets = {
            "login": TextInput(attrs={
                'class': 'input100',
            }),
            "password": TextInput(attrs={
                'class': 'input100',
            })
        }
