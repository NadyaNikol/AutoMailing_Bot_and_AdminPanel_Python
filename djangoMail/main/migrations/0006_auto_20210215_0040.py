# Generated by Django 3.1.4 on 2021-02-14 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210214_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='image_file',
            field=models.ImageField(default='', upload_to='images/%Y/%m/%d', verbose_name='Картинка'),
        ),
    ]
