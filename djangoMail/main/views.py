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
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files.storage import default_storage
import datetime


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def send_message(request):
    all_info = Groups.get_id_groups()
    if all_info is None: all_info = []

    list_info = list(all_info)

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
        form_data = form.data['form']
        image = form.files['image']
        selected_groups = form.data['selected_groups']

        with default_storage.open(image.name, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        # ss = request.FILES['file']

        # form_data = post['data_form']
        # file = post['file']
        # form_data = json.loads(post['data_form'])
        form_data = json.loads(form_data)
        theme = form_data[0]['value']
        text = form_data[1]['value']

        Messages.save_recording(theme, text, settings.MEDIA_ROOT + "\\" + image.name)

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
        if selected_groups != "":
            bot = Bot(token=settings.TOKEN)
            for el in selected_groups:
                bot.send_message(el, "*" + theme + "*\n" + text,
                                 parse_mode='Markdown')
                bot.sendPhoto(el, photo=open(settings.MEDIA_ROOT + '/'+image.name, 'rb'))
                time.sleep(1)
        # return redirect('send_message')
            return JsonResponse({'result': 'ok'})

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
    all_info = Groups.get_id_groups()
    if all_info is None: all_info = []

    list_info = list(all_info)

    if request.method == 'POST' and request.is_ajax():

        req = request.POST
        update_groups = json.loads(req['data'])

        if update_groups is not None and 'result' in update_groups:
            for group in update_groups['result']:
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

    return render(request, 'main/groups.html', {'list_info': list_info})
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
