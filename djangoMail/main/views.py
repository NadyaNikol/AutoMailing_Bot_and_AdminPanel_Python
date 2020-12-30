from django.shortcuts import render, redirect
from .models import Messages, Groups
from .forms import MessageForm
from telegram import Bot
from django.conf import settings
import time


def send_message(request):
    all_id = ''
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            save = request.POST['save']
            # if save is not None:
                # form.save()
            all_id = Groups.get_id_groups()
            if all_id is not None:
                bot = Bot(token=settings.TOKEN)
                for el in all_id:
                    bot.send_message(el, "*" + form.data['theme'] + "*\n" + form.data['text'], parse_mode='Markdown')
                    time.sleep(1)
            return redirect('send_message')
        else:
            error = 'Форма не верна'

    form = MessageForm()

    data = {
        'form': form,
        'all_id': all_id,
    }
    return render(request, 'main/send_message.html', data)
