import numpy as np
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import Messages, Groups
from .forms import MessageForm, GroupsForm
from telegram import Bot
from django.conf import settings
import time


def send_message(request):
    all_info = Groups.get_id_groups()
    list_info = list(all_info)
    if request.method == 'POST':
        form = MessageForm(request.POST)

        try:
            # if form.is_valid():
            # save = request.POST['save']
            # if save is not None:
            a = form.data['theme']            #     form.save()


            b = form.data['text']
            sel = form.data['selected_groups']
            # if list_info is not None:a
            bot = Bot(token=settings.TOKEN)
            # for el in list_info:
            #     bot.send_message(el['id_group'], "*" + form.data['theme'] + "*\n" + form.data['text'], parse_mode='Markdown')
            #     time.sleep(1)
            for el in form.selected_groups:
                bot.send_message(el, "*" + form.data['theme'] + "*\n" + form.data['text'],
                                 parse_mode='Markdown')
                time.sleep(1)
            return redirect('send_message')
            # else:
            #     error = 'Форма не верна'

        except ValidationError as e:
            s = str(e)

    form = MessageForm()

    data = {
        'form': form,
        'list_info': list_info,
    }
    return render(request, 'main/send_message.html', data)

# def update_groups(request):
#     if request.method == 'POST':
#         form = GroupsForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#     form = GroupsForm()
#
#
#     data = {
#         'form': form,
#     }
#     return render(request, 'main/send_message.html', data)
