from django.db import models


class UsersMailing(models.Model):
    login = models.CharField('Логин', max_length=250)
    email = models.EmailField('Email')
    password = models.CharField('Пароль', max_length=50)
    remember_me = models.BooleanField('Запомнить меня', default=False)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    # @staticmethod
    # def get_user(password, login):
    #     if password is not None and login is not None:
    #         return UsersMailing.objects.get(password, login)
