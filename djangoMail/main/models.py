from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError, MultipleObjectsReturned
from django.db import IntegrityError
from django.core.files import File


class Groups(models.Model):
    all_type_groups = [{"id": 0, "name": "ПКО"},
                       {"id": 1, "name": "МКА"},
                       {"id": 2, "name": "ЕКО"}]
    # all_type_groups[0] =
    # all_type_groups[1] =
    # all_type_groups[2] =

    selected_type_group = all_type_groups[0]['id']

    id_group = models.IntegerField(unique=True)
    name = models.CharField('Название группы', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    @staticmethod
    def get_data_groups():
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
            print('такая группа уже существует в бд')
        except MultipleObjectsReturned:
            print('такая группа уже существует в бд')
        except Exception as e:
            print(e)

    @staticmethod
    def save_recording(id_gr, name):
        try:
            new_gr = Groups(id_group=id_gr, name=name)
            new_gr.save()
        except IntegrityError:
            print('не удалось записать группу в бд')
        except Exception as e:
            print(e)


class Messages(models.Model):
    theme = models.CharField('Тема', max_length=250)
    text = models.TextField('Сообщение')
    image_file = models.ImageField('Картинка', upload_to='images/%Y/%m/%d', default='', blank=True, null=True)

    # created_at = models.DateTimeField('Время отправки', auto_now_add=True)

    # file = models.TextField('Файл')

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    @staticmethod
    def save_recording(theme, text, settings_root, name_file=""):
        try:
            if name_file == "":
                new_mess = Messages(theme=theme, text=text)
                new_mess.save()
            else:
                new_mess = Messages(theme=theme, text=text, image_file=name_file)
                f = open(settings_root + "\\" + name_file, 'rb')
                my_file = File(f)
                new_mess.image_file.save(name_file, my_file, save=True)

        except IntegrityError:
            print('не удалось открыть файл')
        except Exception as e:
            print(e)
