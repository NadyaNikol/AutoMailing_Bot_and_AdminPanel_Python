from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from .models import Messages, Groups
from .forms import MessageForm, GroupsForm
from telegram import Bot
from django.conf import settings
import time
import cgitb
import json
import re
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files.storage import default_storage
import datetime


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


def send_message(request):
    try:
        type_of_group_ind = request.GET['type_of_group_ind']
        type_of_group_ind = int(type_of_group_ind)

        if type_of_group_ind != "" and 0 <= type_of_group_ind <= 3:
            Groups.selected_type_group = Groups.all_type_groups[type_of_group_ind]['id']

    except MultiValueDictKeyError as e:
        pass
    except Exception as e:
        pass

    if request.method == 'POST':
        # image = request.FILES.get('image')
        # data_form = request.POST.get('form')
        # selected_groups = request.POST.get('selected_groups')
        #
        # s = settings.MEDIA_ROOT
        # # all_info = Groups.get_id_groups()
        # # list_info = list(all_info)
        # post = request.POST

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
            print(e)

        if image != "":
            try:
                with default_storage.open(image.name, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                name_file = image.name
            except IOError as e:
                print('не удалось открыть файл')
            except Exception as e:
                print(e)
        # ss = request.FILES['file']

        # form_data = post['data_form']
        # file = post['file']
        # form_data = json.loads(post['data_form'])
        form_data = json.loads(form_data)
        theme = form_data[0]['value']
        text = form_data[1]['value']

        if is_save == "true":
            Messages.save_recording(theme, text, settings_root, name_file)

        # form = MessageForm(initial={'theme': theme, 'text': text, 'image_file': settings.MEDIA_ROOT+'/mmm.jpg'})
        # form.save()
        # if theme != "" and text != "":
        #     form = MessageForm(initial={'theme': theme, 'text': text})
        #     # form.save()
        # # selected_groups = json.loads(post['selected_groups'])

        selected_groups = json.loads(selected_groups)

        # map(int, selected_groups)
        # selected_groups = map(int, selected_groups)
        # selected_groups = [int(numeric_string) for numeric_string in selected_groups]
        # try:
        #     if form.is_valid():
        # fd = form.data
        # s = fd['theme']
        # d = fd['text']
        photo_send = ""
        try:
            photo_send = open(settings_root + '/' + image.name, 'rb')
        except IOError as e:
            print('не удалось открыть файл')
        except Exception as e:
            print(e)

        try:
            if selected_groups != "":
                bot = Bot(token=settings.TOKEN)
                for el in selected_groups:
                    bot.send_message(el, "*" + theme + "*\n" + text, parse_mode='Markdown')

                    if photo_send != "":
                        bot.sendPhoto(el, photo=photo_send)
                    time.sleep(1)
                # return redirect('send_message')
                return JsonResponse({'result': 'ok'})
        except Exception as e:
            print(e)
            return JsonResponse({'result': 'Произошла ошибка. Рассылка не была совершена. Повторите попытку'})

        # fd = form.data
        # data = {
        #     # 'form': form,
        #     'list_info': list_info,
        # }
        # # return JsonResponse(data)
        # return render(request, 'main/send_message.html', data)

        # except ObjectDoesNotExist:
        #     error = 'Логин или пароль введены не верно'
        # except MultipleObjectsReturned:
        #     error = 'Логин или пароль введены не верно'

        # form = json.loads(request.POST['result[0][message][chat][id]'])
        # update_groups = request.POST['update_groups']
        # update groups

        # form = list(form.data)
        # result = json.load(form)
        # s = result['result']

        # try:
        # if form.is_valid():
        # save = request.POST['save']
        # if save is not None:
        #     a = form.data['theme']  # form.save()
        #
        #     # ss = form2.getlist('iss')
        #
        #     b = form.data['text']
        #     sel = form.data['selected_groups']
        #     # if list_info is not None:a
        #     bot = Bot(token=settings.TOKEN)
        #     # for el in list_info:
        #     #     bot.send_message(el['id_group'], "*" + form.data['theme'] + "*\n" + form.data['text'], parse_mode='Markdown')
        #     #     time.sleep(1)
        #     for el in form.selected_groups:
        #         bot.send_message(el, "*" + form.data['theme'] + "*\n" + form.data['text'],
        #                          parse_mode='Markdown')
        #         time.sleep(1)
        #     return redirect('send_message')
        #     # else:
        #     #     error = 'Форма не верна'
        #
        # except ValidationError as e:
        #     s = str(e)

    all_info = Groups.get_data_groups()
    if all_info is None: all_info = []

    list_info = list(all_info)

    groupMKA, groupPKO, groupEKO = splitting_into_groups(list_info)

    send_list = []

    if Groups.selected_type_group == Groups.all_type_groups[0]['id']:
        send_list = groupPKO
    elif Groups.selected_type_group == Groups.all_type_groups[1]['id']:
        send_list = groupMKA
    else:
        send_list = groupEKO

    if request.is_ajax():
        return render(request, 'main/groups.html', {'list_info': send_list})

    form = MessageForm()
    data = {
        'form': form,
        # 'list_info': list_info,
        'list_info': send_list,
        'type_group': Groups.all_type_groups,
        'selected_type': Groups.selected_type_group

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

def is_unique_id(list_group, id_group):
    # for i, item in enumerate(list_group):
    #     a[i] = int(item)
    # length = len(list_group)
    # i = 0
    # while i < length:
    for i, item in enumerate(list_group):
        if id_group == item['id_group']:
            return False, i
    return True, -1


def show_groups(request):
    all_info = Groups.get_data_groups()
    if all_info is None:
        all_info = []

    list_info = list(all_info)

    if request.method == 'POST' and request.is_ajax():

        try:
            req = request.POST
            update_groups = json.loads(req['data'])

            if update_groups is not None and 'result' in update_groups:
                for group in update_groups['result']:
                    if 'message' in group:
                        if 'id' in group['message']['chat']:
                            js_id = group['message']['chat']['id']
                            is_unique, index_el = is_unique_id(list_info, js_id)

                            if 'left_chat_participant' in group['message']:
                                if index_el is not -1:
                                    Groups.delete_recording(js_id)
                                    del list_info[index_el]

                            elif js_id is not None:
                                if is_unique:
                                    js_name = group['message']['chat']['title']
                                    Groups.save_recording(js_id, js_name)
                                    list_info.append({'id_group': js_id, 'name': js_name})

        except Exception as e:
            pass

    groupMKA, groupPKO, groupEKO = splitting_into_groups(list_info)

    send_list = []

    if Groups.selected_type_group == Groups.all_type_groups[0]['id']:
        send_list = groupPKO
    elif Groups.selected_type_group == Groups.all_type_groups[1]['id']:
        send_list = groupMKA
    else:
        send_list = groupEKO

    return render(request, 'main/groups.html', {
        'list_info': send_list,
        'selected_type': Groups.selected_type_group
    })
    # return JsonResponse({
    #     'list_info': 'ok'})

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

# def change_type_group(request):

