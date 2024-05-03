# flake8: noqa
import django
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('lib_udc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('number', models.CharField(max_length=15, verbose_name='Номер билета')),
                ('schoolchild_id', models.IntegerField(unique=True, null=True, verbose_name='Ученик', blank=True)),
                ('teacher_id', models.IntegerField(null=True, verbose_name='Учитель', blank=True)),
                ('year', models.CharField(default=2016, max_length=4, verbose_name='Дата регистрации в библиотеке')),
                ('role', models.SmallIntegerField(default=1, verbose_name='Роль', choices=[(1, 'Ученик'), (2, 'Сотрудник'), (None, 'Все')])),
                ('other_libs', models.TextField(max_length=2000, null=True, verbose_name='Другие библиотеки', blank=True)),
                ('favorite_subject', models.TextField(max_length=2000, null=True, verbose_name='Любимый предмет', blank=True)),
                ('circles', models.TextField(max_length=2000, null=True, verbose_name='Кружки', blank=True)),
                ('reading_about', models.TextField(max_length=2000, null=True, verbose_name='О чём читает', blank=True)),
                ('hobby', models.TextField(max_length=2000, null=True, verbose_name='Занятия в свободное время', blank=True)),
                ('is_read', models.SmallIntegerField(default=1, null=True, verbose_name='Сам читает', blank=True, choices=[(0, 'Нет'), (1, 'Да')])),
                ('tech', models.CharField(max_length=10, null=True, verbose_name='Техника чтения', blank=True)),
            ],
            options={
                'db_table': 'library_readers',
                'verbose_name': 'Читатель',
                'verbose_name_plural': 'Читатели',
            },
        ),
        migrations.CreateModel(
            name='Reader2Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('responce_id', models.IntegerField(verbose_name='Отзыв')),
                ('reader', models.ForeignKey(verbose_name='Читатель', to='readers.Reader',
                                             on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'library_reader_responce',
            },
        ),
        migrations.CreateModel(
            name='SearchRequestHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('type', models.SmallIntegerField(verbose_name='тип запроса', choices=[(0, 'Простой поиск'), (1, 'Расширенный поиск')])),
                ('date', models.DateField(verbose_name='дата выполнения запроса')),
                ('simple_request', models.CharField(max_length=300, null=True, verbose_name='текст запроса простого поиска', blank=True)),
                ('book_title', models.CharField(max_length=350, null=True, verbose_name='заглавие', blank=True)),
                ('authors', models.CharField(default='-', max_length=350, null=True, verbose_name='авторы', blank=True)),
                ('subject_id', models.IntegerField(null=True, verbose_name='предмет', blank=True)),
                ('discipline_id', models.IntegerField(null=True, verbose_name='предмет ФГОС', blank=True)),
                ('tags', models.CharField(max_length=350, null=True, verbose_name='ключевые слова', blank=True)),
                ('reader', models.ForeignKey(verbose_name='читатель', to='readers.Reader',
                                             on_delete=django.db.models.deletion.CASCADE)),
                ('udc', models.ForeignKey(verbose_name='раздел УДК', blank=True, to='lib_udc.LibraryUDC', null=True,
                                          on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'lib_reader_search_history',
            },
        ),
        migrations.CreateModel(
            name='TeacherReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('reader', models.ForeignKey(verbose_name='читатель', to='readers.Reader',
                                             on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'lib_teacher_review',
            },
        ),
    ]
