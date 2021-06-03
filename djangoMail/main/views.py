import os

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Messages, Groups
from .forms import MessageForm
from telegram import Bot
from django.conf import settings
import time
import json
import re
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)


def splitting_into_groups(list_group):
    groupMKA = []
    groupPKO = []
    groupEKO = []

    for i, item in enumerate(list_group):
        str_name = list_group[i]['name'] = str(list_group[i]['name']).upper()
        # EKO in the english and in the russian languages
        if str_name.upper().find("EKO") != -1 or \
                str_name.upper().find("ЕКО") != -1:
            groupEKO.append(list_group[i])

        elif (re.search(r'\d{4}', str_name)) is not None or (
                re.search(r'^\D{2}\d{2}$', str_name)) is not None:
            groupMKA.append(list_group[i])

        else:
            groupPKO.append(list_group[i])

    return groupMKA, groupPKO, groupEKO


def get_send_list(list_info):
    groupMKA, groupPKO, groupEKO = splitting_into_groups(list_info)

    if Groups.selected_type_group == Groups.all_type_groups[0]['id']:
        send_list = groupPKO
    elif Groups.selected_type_group == Groups.all_type_groups[1]['id']:
        send_list = groupMKA
    else:
        send_list = groupEKO

    return send_list


def is_unique_id(list_group, id_group, name_group):
    for i, item in enumerate(list_group):
        if id_group == item['id_group'] and name_group != item['name']:
            return False, True, i
        elif id_group == item['id_group']:
            return False, False, i
    return True, False, -1


def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        selected_groups = form.data['selected_groups']

        if selected_groups == '[]':
            return JsonResponse({'result': 'Выберите группу'})

        form_data = form.data['form']
        is_save = form.data['is_save']
        settings_root = settings.MEDIA_ROOT
        name_file = ""
        image = ""
        try:
            image = form.files['image']
        except Exception as e:
            logger.warning(e)

        if image != "":
            try:
                with default_storage.open(image.name, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                # name_file = image.name
            except IOError as e:
                logger.warning('не удалось открыть файл')
            except Exception as e:
                logger.warning(e)

        form_data = json.loads(form_data)
        theme = form_data[0]['value']
        text = form_data[1]['value']

        if is_save == "true":
            Messages.save_recording(theme, text)

        selected_groups = json.loads(selected_groups)
        # photo_send = ""
        # try:
        #     photo_send = open(settings_root + '/' + image.name, 'rb')
        # except IOError as e:
        #     logger.warning('не удалось открыть файл')
        # except Exception as e:
        #     logger.warning(e)
        el_error = ''
        try:
            bot = Bot(token=settings.TOKEN)
            for el in selected_groups:
                el_error = el
                bot.send_message(el, "*" + theme + "*\n" + text, parse_mode='Markdown')

                if image != "":
                    bot.sendPhoto(el, photo=open(settings_root + '/' + image.name, 'rb'))
                time.sleep(0.5)

            if image != "":
                os.remove(settings_root + '\\' + image.name)
            return JsonResponse({'result': 'ok'})
        except Exception as e:
            logger.warning(e)
            if el_error != '':
                name_group_error = Groups.get_name_from_id_group(el_error)
                if name_group_error is not None:
                    return JsonResponse(
                        {'result': 'Произошла ошибка на группе ' + name_group_error +
                                   ' Повторите попытку, выбрав все группы после нее включительно'})
            return JsonResponse({'result': 'Произошла ошибка. Рассылка не была совершена полностью. Повторите попытку'})

    list_info = Groups.get_data_groups()
    send_list = get_send_list(list_info)

    if request.is_ajax():
        return render(request, 'main/groups.html', {'list_info': send_list})

    form = MessageForm()
    data = {
        'form': form,
        'list_info': send_list,
        'type_group': Groups.all_type_groups,
        'selected_type': Groups.selected_type_group
    }

    return render(request, 'main/send_message.html', data)


def show_groups(request):
    list_info = Groups.get_data_groups()

    if request.method == 'POST' and request.is_ajax():

        try:
            req = request.POST
            update_groups = json.loads(req['data'])

            if update_groups is not None and 'result' in update_groups:
                for group in update_groups['result']:
                    if 'message' in group:
                        if 'id' and 'title' in group['message']['chat']:
                            js_id = group['message']['chat']['id']
                            js_name = group['message']['chat']['title']
                            is_unique, is_update, index_el = is_unique_id(list_info, js_id, js_name)

                            if 'left_chat_participant' in group['message'] \
                                    or 'status' in group and 'status' == 'left':
                                if index_el != -1:
                                    Groups.delete_recording(js_id)
                                    del list_info[index_el]

                            elif js_id is not None:
                                if is_unique:
                                    js_name = group['message']['chat']['title']
                                    Groups.save_recording(js_id, js_name)
                                    list_info.append({'id_group': js_id, 'name': js_name})

                                elif is_update:
                                    js_name = group['message']['chat']['title']
                                    Groups.update_recording(js_id, js_name)
                                    list_info[index_el] = {'id_group': js_id, 'name': js_name}

                    elif 'my_chat_member' in group:
                        chat_member = ''
                        if 'new_chat_member' in group['my_chat_member']:
                            chat_member = 'new_chat_member'
                        elif 'old_chat_member' in group['my_chat_member']:
                            chat_member = 'old_chat_member'

                        if chat_member != '':
                            if 'status' in group['my_chat_member'][chat_member] \
                                    and group['my_chat_member'][chat_member]['status'] == 'left':
                                js_id = group['my_chat_member']['chat']['id']
                                js_name = group['my_chat_member']['chat']['title']
                                is_unique, is_update, index_el = is_unique_id(list_info, js_id, js_name)
                                if index_el != -1:
                                    Groups.delete_recording(js_id)
                                    del list_info[index_el]

        except Exception as e:
            logger.warning(e)

    send_list = get_send_list(list_info)

    return render(request, 'main/groups.html', {
        'list_info': send_list,
        'selected_type': Groups.selected_type_group
    })


# change type groups (MKA, PKO, EKO) #
def change_group_type(request):
    type_of_group_ind = request.GET['type_of_group_ind']

    if type_of_group_ind != '':
        type_of_group_ind = int(type_of_group_ind)

        if type_of_group_ind != "" and 0 <= type_of_group_ind <= 3:
            Groups.selected_type_group = Groups.all_type_groups[type_of_group_ind]['id']
            return redirect('send_message')


# open modal and get saved messages
def get_saved_messages(request):
    if request.is_ajax():
        saved_messages = Messages.get_data_messages()
        return JsonResponse({'saved_messages': saved_messages, 'result': 'ok'})
    return JsonResponse({'result': 'error'})


# delete selected message in the modal
def delete_message(request):
    delete_mess = request.GET['delete_mess']

    if delete_mess == '[]':
        return JsonResponse({'result': 'error'})

    else:
        delete_mess = json.loads(delete_mess)
        for item in delete_mess:
            Messages.delete_recording(item)

        return JsonResponse({'result': 'ok'})
