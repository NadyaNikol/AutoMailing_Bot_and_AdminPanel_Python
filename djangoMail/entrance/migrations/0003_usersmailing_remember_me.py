# Generated by Django 3.1.4 on 2021-01-06 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0002_auto_20201221_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersmailing',
            name='remember_me',
            field=models.BooleanField(default=False, verbose_name='Запомнить меня'),
        ),
    ]
