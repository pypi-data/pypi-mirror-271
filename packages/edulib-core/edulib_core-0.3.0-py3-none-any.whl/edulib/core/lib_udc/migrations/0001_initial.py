# flake8: noqa
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryUDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('code', models.CharField(max_length=32, verbose_name='Код', db_index=True)),
                ('name', models.CharField(db_index=True, max_length=900, null=True, verbose_name='Наименование', blank=True)),
            ],
            options={
                'db_table': 'lib_udc',
                'verbose_name': 'Разделы УДК',
            },
        ),
    ]
