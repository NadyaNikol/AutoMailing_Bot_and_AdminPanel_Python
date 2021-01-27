from .models import Messages, Groups
from django.forms import ModelForm, TextInput, Textarea


class MessageForm(ModelForm):
    class Meta:
        model = Messages
        fields = ['theme', 'text']

        widgets = {
            "theme": TextInput(attrs={
                'class': 'input100',
            }),
            "text": Textarea(attrs={
                'class': 'input100',
            })
        }


class GroupsForm(ModelForm):
    class Meta:
        model = Groups
        fields = ['id_group', 'name']

        widgets = {
            "id_group": TextInput(attrs={
                'class': 'input100'
            }),
            "name": TextInput(attrs={
                'class': 'input100'
            }),
        }
