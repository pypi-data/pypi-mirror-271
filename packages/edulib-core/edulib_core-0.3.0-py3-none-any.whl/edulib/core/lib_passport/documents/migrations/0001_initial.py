from django.db import (
    migrations,
    models,
)

import edulib.core.base.files


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LibPassportDocuments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('doc_type', models.PositiveIntegerField(blank=True, null=True, verbose_name='Тип документа', choices=[(1, 'Норативно-правовая база'), (2, 'Документы учета работы библиотеки')])),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('document', models.FileField(max_length=255, upload_to=edulib.core.base.files.upload_file_handler, null=True, verbose_name='Файл', blank=True)),
            ],
            options={
                'db_table': 'library_passport_documents',
                'verbose_name': 'Документы библиотеки',
                'verbose_name_plural': 'Документы библиотеки',
            },
        ),
    ]
