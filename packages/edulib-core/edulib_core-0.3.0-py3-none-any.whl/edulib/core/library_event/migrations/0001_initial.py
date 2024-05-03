# flake8: noqa
import django
from django.db import (
    migrations,
    models,
)

import edulib.core.base.files


class Migration(migrations.Migration):

    dependencies = [
        ('lib_passport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('place', models.CharField(max_length=100, verbose_name='Место проведения')),
                ('date_begin', models.DateField(verbose_name='Дата проведения')),
                ('date_end', models.DateField(null=True, verbose_name='по', blank=True)),
                ('participants', models.CharField(max_length=100, verbose_name='Заинтересованная аудитория/участники')),
                ('file', models.FileField(upload_to=edulib.core.base.files.upload_file_handler, max_length=255, verbose_name='Приложения', blank=True)),
                ('description', models.TextField(null=True, verbose_name='Описание', blank=True)),
                ('library', models.ForeignKey(verbose_name='Учебный класс', to='lib_passport.LibPassport',
                                              on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
