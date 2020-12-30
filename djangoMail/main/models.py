from django.db import models


class Groups(models.Model):
    id_group = models.IntegerField()
    name = models.CharField('Название группы', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    @staticmethod
    def get_id_groups():
        all_id = Groups.objects.values_list('id_group', flat=True)
        return all_id


class Messages(models.Model):
    theme = models.CharField('Тема', max_length=250)
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Время отправки', auto_now_add=True)

    # file = models.TextField('Файл')

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
