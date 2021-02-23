from .models import Messages, Groups
from django.forms import ModelForm, TextInput, Textarea, FileInput


class MessageForm(ModelForm):
    class Meta:
        model = Messages
        fields = ['theme', 'text', 'image_file']

        widgets = {
            "theme": TextInput(attrs={
                # 'class': 'input100',
                'class': 'message_input theme_input'
            }),
            "text": Textarea(attrs={
                # 'class': 'input100',
                'class': 'message_input'
            }),
            "image_file": FileInput(attrs={
                'class': "form-control form-control-sm "
            }),
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
