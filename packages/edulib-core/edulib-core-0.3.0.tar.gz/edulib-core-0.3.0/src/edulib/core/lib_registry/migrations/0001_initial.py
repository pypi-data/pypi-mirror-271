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
        ('lib_udc', '0001_initial'),
        ('lib_example_types', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibMarkInformProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('code', models.CharField(max_length=20, verbose_name='Код', db_index=True)),
                ('name', models.CharField(db_index=True, max_length=200, null=True, verbose_name='Наименование', blank=True)),
            ],
            options={
                'db_table': 'lib_mark_prod',
                'verbose_name': 'Знак информационной продукции',
            },
        ),
        migrations.CreateModel(
            name='LibRegistryEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('book_title', models.CharField(max_length=350, verbose_name='заглавие')),
                ('authors', models.CharField(default='-', max_length=350, verbose_name='авторы')),
                ('subject_id', models.IntegerField(null=True, verbose_name='предмет', blank=True)),
                ('discipline_id', models.IntegerField(null=True, verbose_name='предмет ФГОС', blank=True)),
                ('tags', models.CharField(max_length=350, null=True, verbose_name='ключевые слова', blank=True)),
                ('short_info', models.CharField(max_length=1000, null=True, verbose_name='краткое описание', blank=True)),
                ('cover', models.ImageField(max_length=3072, upload_to=edulib.core.base.files.upload_file_handler, null=True, verbose_name='Обложка', blank=True)),
                ('school_id', models.IntegerField(verbose_name='школа')),
                ('filename', models.FileField(max_length=255, upload_to=edulib.core.base.files.upload_named_handler, null=True, verbose_name='Файл', blank=True)),
                ('age_tag', models.ForeignKey(verbose_name='знак информационной продукции', blank=True,
                                              to='lib_registry.LibMarkInformProduct', null=True,
                                              on_delete=django.db.models.deletion.CASCADE)),
                ('type', models.ForeignKey(verbose_name='тип библиотечного экземпляра',
                                           to='lib_example_types.LibraryExampleType',
                                           on_delete=django.db.models.deletion.CASCADE)),
                ('udc', models.ForeignKey(verbose_name='раздел УДК', blank=True, to='lib_udc.LibraryUDC', null=True,
                                          on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'lib_registry',
            },
        ),
        migrations.CreateModel(
            name='LibRegistryExample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('inv_number', models.CharField(max_length=20, unique=True, null=True, verbose_name='инвентарный номер', blank=True)),
                ('card_number', models.CharField(max_length=20, null=True, verbose_name='номер карточки учета', blank=True)),
                ('inflow_date', models.DateField(verbose_name='дата поступления')),
                ('edition', models.CharField(max_length=50, null=True, verbose_name='издание', blank=True)),
                ('edition_place', models.CharField(max_length=50, verbose_name='место издания')),
                ('pub_office', models.CharField(max_length=100, verbose_name='издательство')),
                ('edition_year', models.PositiveSmallIntegerField(verbose_name='год издания')),
                ('duration', models.CharField(max_length=10, verbose_name='количество страниц / длительность')),
                ('book_code', models.CharField(max_length=20, verbose_name='шифр книги')),
                ('max_date', models.CharField(max_length=5, null=True, verbose_name='максимальный срок выдачи', blank=True)),
                ('price', models.CharField(max_length=5, null=True, verbose_name='стоимость', blank=True)),
                ('fin_source', models.SmallIntegerField(blank=True, null=True, verbose_name='источник финансирования', choices=[(0, 'федеральный бюджет'), (1, 'региональный бюджет'), (2, 'муниципальный бюджет'), (3, 'средства учреждения'), (4, 'средства спонсоров')])),
                ('writeoff_date', models.DateField(null=True, verbose_name='дата списания', blank=True)),
                ('writeoff_reason', models.SmallIntegerField(blank=True, null=True, verbose_name='причина списания', choices=[(0, 'Устаревание по содержанию'), (1, 'Пропажа из фондов открытого доступа'), (2, 'Утеря читателями'), (3, 'Хищение'), (4, 'Бедствие стихийного и техногенного характера'), (5, 'По неустановленным причинам (недостача).'), (6, 'Физический износ'), (7, 'Книгообмен с другой библиотекой'), (8, 'Иное')])),
                ('act_number', models.CharField(max_length=20, null=True, verbose_name='номер акта приема / передачи', blank=True)),
                ('act_date', models.DateField(null=True, verbose_name='от', blank=True)),
                ('exchanged_example', models.ForeignKey(verbose_name='экземпляр заменен', blank=True,
                                                        to='lib_registry.LibRegistryExample', null=True,
                                                        on_delete=django.db.models.deletion.CASCADE)),
                ('lib_reg_entry', models.ForeignKey(verbose_name='карточка учета экземпляра',
                                                    to='lib_registry.LibRegistryEntry',
                                                    on_delete=django.db.models.deletion.CASCADE)),
                ('library', models.ForeignKey(blank=True, to='lib_passport.LibPassport', null=True,
                                              on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'lib_reg_examples',
            },
        ),
    ]
