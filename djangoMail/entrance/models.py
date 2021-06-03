from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import logging

logger = logging.getLogger(__name__)


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

    @staticmethod
    def get_data_user(password, login):
        try:
            user = UsersMailing.objects.get(password=password, login=login)
            return user
        except ObjectDoesNotExist:
            logger.warning("Object user Does Not Exist")
            return None
