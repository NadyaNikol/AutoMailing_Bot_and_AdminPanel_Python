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
        # all_id = Groups.objects.values_list('id_group', flat=True)
        all_id = Groups.objects.values('id_group', 'name')
        return all_id

    @staticmethod
    def delete_recording(id_gr):
        return Groups.objects.filter(id_group=id_gr).delete()

    @staticmethod
    def save_recording(id_gr, name):
        new_gr = Groups(id_group=id_gr, name=name)
        return new_gr.save()

class Messages(models.Model):
    theme = models.CharField('Тема', max_length=250)
    text = models.TextField('Сообщение')

    # created_at = models.DateTimeField('Время отправки', auto_now_add=True)

    # file = models.TextField('Файл')

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
