from django.contrib import admin

from .models import Groups, Messages
from .forms import MessageForm, GroupsForm


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_group', 'name')
    form = GroupsForm


@admin.register(Messages)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'text', 'created_at')
    # form = MessageForm
