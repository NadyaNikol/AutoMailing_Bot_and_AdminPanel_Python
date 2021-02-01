# Generated by Django 3.1.4 on 2020-12-21 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=250, verbose_name='Логин')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('password', models.CharField(max_length=50, verbose_name='Пароль')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]