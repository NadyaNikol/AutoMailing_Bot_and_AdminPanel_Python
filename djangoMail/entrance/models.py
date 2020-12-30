from django.db import models


class UsersMailing(models.Model):
    login = models.CharField('Логин', max_length=250)
    email = models.EmailField('Email')
    password = models.CharField('Пароль', max_length=50)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


