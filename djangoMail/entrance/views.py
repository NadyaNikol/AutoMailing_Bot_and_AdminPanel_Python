from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from djangoMail import settings
from .models import UsersMailing
from .forms import EntranceForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.http import JsonResponse


def home(request):
    if request.session.has_key('username') and request.session.has_key('password'):
        username = request.session['username']
        password = request.session['password']
        context_dict = {'username': username, 'password': password}
        return render(request, 'sadmin/login.html', context=context_dict)
    else:
        context_dict = {'username': '', 'password': ''}
        return render(request, 'sadmin/login.html', context=context_dict)


def entrance(request):
    # if request.method == "POST":
    #     form = EntranceForm(request.POST)
    #     if form.is_valid():
    #         login = form.cleaned_data['login']
    #         password = form.cleaned_data['password']
    #         remember_me = form.cleaned_data['remember_me']
    #         user = authenticate(login=login, password=password)
    #         if user:
    #             auth_login(request, user)
    #             if not remember_me:
    #                 request.session.set_expiry(
    #                     0)  # <-- Here if the remember me is False, that is why expiry is set to 0 seconds. So it will automatically close the session after the browser is closed.
    #
    #             # else browser session will be as long as the session  cookie time "SESSION_COOKIE_AGE"
    #             return redirect('send_message')
    #     # if request.POST['is_remember_check'] == 'true':
    #     #     request.session['login'] = request.POST['login']
    #     #     request.session['password'] = request.POST['password']
    #     #
    #     # user = authenticate(login=request.POST['login'], password=request.POST['password'])
    #     #
    #     # if user is not None:
    #     #     return JsonResponse({'result': request.POST, 'status': True})
    #     # else:
    #     #     return JsonResponse({'result': request.POST, 'status': False})
    #
    # form = EntranceForm()
    # data = {
    #     'form': form,
    #     # 'error': error,
    #     # 's': request.session
    # }
    # return render(request, 'entrance/index.html', data)

    error = ''
    if request.method == 'POST':
        form = EntranceForm(request.POST)
        try:

            if form.is_valid():
                # password = form.data['password']
                # login = form.data['login']
                # user = UsersMailing.objects.get(password=password, login=login)
                # try:
                #     remember = request.POST['remember_me']
                #     if remember:
                #         settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                # except MultiValueDictKeyError:
                #     is_private = False
                #     settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True

                # request.session['login'] = request.POST['login']
                # request.session['password'] = request.POST['password']
                #
                fd = form.data
                password = fd['password']
                login = fd['login']
                remember_me = fd['remember_me'] if fd.get('remember_me') else False
                user = UsersMailing.objects.get(password=password, login=login)

                if user:
                    if not fd.get('remember_me'):
                        request.session.set_expiry(-1209600)
                        request.session.modified = True
                        # request.session['remember_me'] = remember_me
                    # auth_login(request, user)
                    else:
                        request.session['login'] = login
                        request.session['password'] = password
                        request.session['remember_me'] = remember_me
                        request.session.set_expiry(1209600)

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                return redirect('send_message')

        #     if form.is_valid():
        #         if form.save(request):
        #             return redirect('send_message')
        #     else:
        #         error = 'Форма не верна'
        except ObjectDoesNotExist:
            error = 'Логин или пароль введены не верно'
        except MultipleObjectsReturned:
            error = 'Логин или пароль введены не верно'
        finally:
            form = EntranceForm()
            data = {
                'form': form,
                'error': error
                # 's': request.session
            }
            return render(request, 'entrance/index.html', data)

    else:
        form = EntranceForm()

        request.session.set_test_cookie()

        if request.session.has_key('password') and request.session.has_key('login'):
            rs = request.session
            login = rs['login']
            password = rs['password']
            remember_me = rs['remember_me']
            # context_dict = {'password': password}
            form = EntranceForm(initial={'login': login, 'password': password, 'remember_me': remember_me})
            data = {
                'form': form
                # 'error': error,
                # 's': request.session
            }
            return render(request, 'entrance/index.html', data)
        else:
            # context_dict = {'password': ''}
            # return render(request, 'entrance/index.html', context=context_dict)
            data = {
                'form': form
                # 'error': error,
                # 's': request.session
            }
            return render(request, 'entrance/index.html', data)

        # if request.session.has_key('password') and request.session.has_key('login'):
        #     form.data['password'] = request.session['password']
        #     form.data['login'] = request.session['login']
        #
        #     data = {
        #         'form.login': request.session['login'],
        #         'form.password': request.session['password'],
        #         'error': error,
        #         's': request.session
        #     }
        #     return render(request, 'entrance/index.html', data)

    # request.session.set_test_cookie()
    #
    # data = {
    #     'form': form,
    #     'error': error,
    #     # 's': request.session
    # }
    # return render(request, 'entrance/index.html', data)
