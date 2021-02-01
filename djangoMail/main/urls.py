from django.urls import path
from . import views

urlpatterns = [
    path('', views.send_message, name='send_message'),
    path('groups', views.show_groups, name='show_groups'),
]