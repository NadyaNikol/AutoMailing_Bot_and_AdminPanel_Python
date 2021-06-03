from django.shortcuts import render, redirect
from .models import UsersMailing
from .forms import EntranceForm
import logging

logger = logging.getLogger(__name__)


def entrance(request):
    if request.method == 'POST':
        form = EntranceForm(request.POST)
        try:

            if form.is_valid():

                fd = form.data
                password = fd['password']
                login = fd['login']
                remember_me = fd.get('remember_me') if fd.get('remember_me') else False
                user = UsersMailing.get_data_user(password, login)
                rs = request.session

                if user:
                    if not fd.get('remember_me'):
                        rs.set_expiry(-1209600)
                        # rs.modified = True

                    else:
                        # if request.session.test_cookie_worked():
                        #     request.session.delete_test_cookie()

                        rs['login'] = login
                        rs['password'] = password
                        rs['remember_me'] = remember_me
                        rs.set_expiry(1209600)

                    return redirect('send_message')

                else:
                    error = 'Логин или пароль введены не верно'
                    form = EntranceForm()
                    data = {
                        'form': form,
                        'error': error
                    }
                    return render(request, 'entrance/index.html', data)

        except Exception as e:
            logger.warning(e)

    else:
        form = EntranceForm()

        request.session.set_test_cookie()
        rs = request.session

        if rs.has_key('password') and rs.has_key('login'):

            login = rs['login']
            password = rs['password']
            remember_me = rs['remember_me']
            form = EntranceForm(initial={'login': login, 'password': password})
            data = {
                'form': form,
                'remember_me': remember_me
            }
            return render(request, 'entrance/index.html', data)
        else:
            data = {
                'form': form,
            }
            return render(request, 'entrance/index.html', data)
