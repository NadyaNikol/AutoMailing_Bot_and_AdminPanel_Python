from django.shortcuts import render, redirect
from .models import UsersMailing
from .forms import EntranceForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def entrance(request):
    error = ''
    if request.method == 'POST':
        form = EntranceForm(request.POST)
        try:
            p = UsersMailing.objects.get(password=form.data['password'],
                                         login=form.data['login'])
            return redirect('send_message')

            # if form.is_valid():
            #     if form.save():
            #         return redirect('send_message')
            # else:
            #     error = 'Форма не верна'
        except ObjectDoesNotExist:
            error = 'Логин или пароль введены не верно'
        except MultipleObjectsReturned:
            error = 'Логин или пароль введены не верно'
    form = EntranceForm()

    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'entrance/index.html', data)
