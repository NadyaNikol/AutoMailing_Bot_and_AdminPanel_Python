from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Messages, Groups
from .forms import MessageForm, GroupsForm
from telegram import Bot
from django.conf import settings
import time
import cgitb
import json


def send_message(request):
    all_info = Groups.get_id_groups()
    list_info = list(all_info)
    if request.method == 'POST' and request.is_ajax():
        req = request.POST
        update_groups = json.loads(req['data'])
        form = MessageForm(req)

        if update_groups['result'] is not None:
            for group in update_groups['result']:
                js_id = group['message']['chat']['id']

                if 'left_chat_participant' in group['message']:
                    Groups.delete_recording(js_id)

                elif js_id is not None and js_id not in list_info:
                    js_name = group['message']['chat']['title']
                    Groups.save_recording(js_id, js_name)

        # type = ret['type']
        # list1 = json.loads(ret['data'])
        # form = request.POST
        # i = 0
        # while True:
        #     if 'result[' + str(i) + '][message][chat][id]' in form:
        #         js_id = json.loads(form['result[' + str(i) + '][message][chat][id]'])
        #
        #         if 'result[' + str(i) + '][message][left_chat_participant][id]' in form:
        #             Groups.delete_recording(js_id)
        #
        #         elif js_id is not None and js_id not in list_info:
        #             js_name = form['result[' + str(i) + '][message][chat][title]']
        #             Groups.save_recording(js_id, js_name)
        #
        #         i += 1
        #     else:
        #         break

        # data = {
        #     'list_info': list_info,
        # }
        # return JsonResponse(data)
        all_info = Groups.get_id_groups()
        list_info = list(all_info)

        data = {
            'form': form,
            'list_info': list_info,
        }
        return JsonResponse(data)

        # form = json.loads(request.POST['result[0][message][chat][id]'])
        # update_groups = request.POST['update_groups']
        # update groups

        # form = list(form.data)
        # result = json.load(form)
        # s = result['result']

        try:
            # if form.is_valid():
            # save = request.POST['save']
            # if save is not None:
            a = form.data['theme']  # form.save()

            # ss = form2.getlist('iss')

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
