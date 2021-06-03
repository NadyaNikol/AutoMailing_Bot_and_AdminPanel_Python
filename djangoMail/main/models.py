from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError, MultipleObjectsReturned
from django.db import IntegrityError
from django.core.files import File
import logging

logger = logging.getLogger(__name__)


class Groups(models.Model):
    all_type_groups = [{"id": 0, "name": "ПКО"},
                       {"id": 1, "name": "МКА"},
                       {"id": 2, "name": "ЕКО"}]

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
            all_id = Groups.objects.values('id_group', 'name')
            if all_id is None: all_id = []
            all_id = list(all_id)
            return all_id
        except ObjectDoesNotExist:
            logger.warning("Object group Does Not Exist")
            return None
        except Exception as e:
            logger.warning(e)
            return None

    @staticmethod
    def delete_recording(id_gr):
        try:
            Groups.objects.filter(id_group=id_gr).delete()
        except ObjectDoesNotExist:
            logger.warning('Object group Does Not Exist')
        except MultipleObjectsReturned:
            logger.warning('Multiple Objects group Returned')
        except Exception as e:
            logger.warning(e)
            return None

    @staticmethod
    def save_recording(id_gr, name):
        try:
            new_gr = Groups(id_group=id_gr, name=name)
            new_gr.save()
        except IntegrityError:
            logger.warning('Integrity group Error')
        except Exception as e:
            logger.warning(e)

    @staticmethod
    def update_recording(id_gr, name):
        try:
            Groups.objects.filter(id_group=id_gr).update(name=name)
        except IntegrityError:
            logger.warning('Integrity group Error')
        except Exception as e:
            logger.warning(e)

    @staticmethod
    def get_name_from_id_group(id_gr):
        try:
            name = Groups.objects.get(id_group=id_gr).name
            return name
        except ObjectDoesNotExist:
            logger.warning("Object group Does Not Exist")
            return None
        except Exception as e:
            logger.warning(e)
            return None


class Messages(models.Model):
    theme = models.CharField('Тема', max_length=250)
    text = models.TextField('Сообщение')
    image_file = models.ImageField('Картинка', upload_to='images/%Y/%m/%d', default='', blank=True, null=True)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    @staticmethod
    def save_recording(theme, text):
        try:
            # if name_file == "":
            new_mess = Messages(theme=theme, text=text)
            new_mess.save()
            # else:
            #     new_mess = Messages(theme=theme, text=text, image_file=name_file)
            #     f = open(settings_root + "\\" + name_file, 'rb')
            #     my_file = File(f)
            #     new_mess.image_file.save(name_file, my_file, save=True)

        except IntegrityError:
            logger.warning('не удалось открыть файл')
        except Exception as e:
            logger.warning(e)

    @staticmethod
    def delete_recording(mess_id):
        try:
            mess = Messages(id=mess_id)
            mess.delete()

        except IntegrityError:
            logger.warning('не удалось удалить сообщение')
        except Exception as e:
            logger.warning(e)

    @staticmethod
    def get_data_messages():
        try:
            all_data = Messages.objects.values()
            if all_data is None: all_data = []
            all_data = list(all_data)
            return all_data
        except ObjectDoesNotExist:
            logger.warning('Object mess Does Not Exist')
            return None
