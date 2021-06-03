from django.urls import path
from . import views

urlpatterns = [
    path('', views.send_message, name='send_message'),
    path('groups', views.show_groups, name='show_groups'),
    path('delete-message', views.delete_message, name='delete_message'),
    path('change-group', views.change_group_type, name='change_group_type'),
    path('modal-message', views.get_saved_messages, name='get_saved_messages')
]