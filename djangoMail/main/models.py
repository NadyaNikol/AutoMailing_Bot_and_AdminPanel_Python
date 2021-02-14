from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError, MultipleObjectsReturned
from django.db import IntegrityError
from django.core.files import File


class Groups(models.Model):
    id_group = models.IntegerField(unique=True)
    name = models.CharField('Название группы', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    @staticmethod
    def get_id_groups():
        try:
            # all_id = Groups.objects.values_list('id_group', flat=True)
            all_id = Groups.objects.values('id_group', 'name')
            return all_id
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_recording(id_gr):
        try:
            Groups.objects.filter(id_group=id_gr).delete()
        except ObjectDoesNotExist:
            pass
        except MultipleObjectsReturned:
            pass

    @staticmethod
    def save_recording(id_gr, name):
        try:
            new_gr = Groups(id_group=id_gr, name=name)
            new_gr.save()
        except IntegrityError:
            pass


class Messages(models.Model):
    theme = models.CharField('Тема', max_length=250)
    text = models.TextField('Сообщение')
    image_file = models.ImageField('Картинка', upload_to='images/%Y/%m/%d', default='')

    # created_at = models.DateTimeField('Время отправки', auto_now_add=True)

    # file = models.TextField('Файл')

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    @staticmethod
    def save_recording(theme, text, image_file):
        try:
            new_mess = Messages(theme=theme, text=text, image_file=image_file)
            f = open(image_file, 'rb')
            myfile = File(f)
            n = myfile.name
            new_mess.image_file.save('mmm.jpg', myfile, save=True)
            # new_mess.save()
        except IntegrityError:
            pass
