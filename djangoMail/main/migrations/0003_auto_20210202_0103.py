# Generated by Django 3.1.4 on 2021-02-01 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='id_group',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='text',
            field=models.TextField(verbose_name='Сообщение'),
        ),
    ]
