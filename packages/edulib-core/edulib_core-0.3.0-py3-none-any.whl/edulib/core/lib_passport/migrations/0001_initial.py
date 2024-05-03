# flake8: noqa
import re

import django.core.validators
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
        ('cleanup_days', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibPassport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, verbose_name='Внешний ключ', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания', db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения', db_index=True)),
                ('school_id', models.IntegerField(verbose_name='id школы')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('date_found_month', models.SmallIntegerField(default=1, verbose_name='Дата основания (месяц)', choices=[(1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'), (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'), (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')])),
                ('date_found_year', models.PositiveSmallIntegerField(null=True, verbose_name='Дата основания (год)', blank=True)),
                ('library_chief_id', models.IntegerField(null=True, verbose_name='Зав. библиотеки', blank=True)),
                ('is_address_match', models.BooleanField(default=False, verbose_name='Адрес совпадает с адресом ОУ')),
                ('f_address_place', models.CharField(blank=True, max_length=36, null=True, verbose_name='Населенный пункт', validators=[django.core.validators.RegexValidator(regex=re.compile(b'^$|^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', 2), message='Указан неверный код адресного объекта ФИАС')])),
                ('f_address_street', models.CharField(blank=True, max_length=36, null=True, verbose_name='Улица', validators=[django.core.validators.RegexValidator(regex=re.compile(b'^$|^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', 2), message='Указан неверный код адресного объекта ФИАС')])),
                ('f_address_house', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(re.compile(r'^[0-9а-яёА-Я\/\-]{1,10}$', 34), message='Проверьте правильность заполнения поля')])),
                ('f_address_house_guid', models.CharField(blank=True, max_length=36, null=True, verbose_name='Дом', validators=[django.core.validators.RegexValidator(regex=re.compile(b'^$|^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', 2), message='Указан неверный код адресного объекта ФИАС')])),
                ('f_address_corps', models.CharField(blank=True, max_length=2, null=True, verbose_name='Корпус', validators=[django.core.validators.RegexValidator(re.compile('^[0-9а-яё]{,2}$', 34), message='Проверьте правильность заполнения поля')])),
                ('f_address_full', models.CharField(max_length=200, null=True, blank=True)),
                ('f_address_zipcode', models.CharField(max_length=10, null=True, blank=True)),
                ('is_telephone_match', models.BooleanField(default=False, verbose_name='Телефон совпадает с телефоном ОУ')),
                ('telephone', models.CharField(max_length=50, null=True, blank=True)),
                ('is_email_match', models.BooleanField(default=False, verbose_name='Email совпадает с email ОУ')),
                ('email', models.CharField(max_length=50, null=True, blank=True)),
                ('is_abonement', models.BooleanField(default=True, verbose_name='Абонемент')),
                ('is_reading_room', models.BooleanField(default=True, verbose_name='Читальный зал')),
                ('reading_room_type', models.PositiveIntegerField(blank=True, null=True, verbose_name='Тип читальногой зала', choices=[(1, 'совмещен с абонементом'), (2, 'отдельный')])),
                ('is_lib_store', models.BooleanField(default=True, verbose_name='Книгохранилище')),
                ('book_fund', models.BigIntegerField(null=True, verbose_name='Книжный фонд (экз.)', blank=True)),
                ('schoolbook_fund', models.BigIntegerField(null=True, verbose_name='Учебники (экз.)', blank=True)),
                ('main_fund', models.BigIntegerField(null=True, verbose_name='Основной фонд (экз.)', blank=True)),
                ('is_media', models.BooleanField(default=False, verbose_name='Медиатека')),
                ('is_pc_base', models.BooleanField(default=False, verbose_name='На базе компьютерного класса')),
                ('media_pc_cnt', models.BigIntegerField(null=True, verbose_name='Кол-во компьютеров для пользования медиатекой', blank=True)),
                ('is_access_internet', models.BooleanField(default=False, verbose_name='Доступ в сеть Интернет')),
                ('mediafiles_total', models.BigIntegerField(null=True, verbose_name='Медиафайлы (экз.)', blank=True)),
                ('mediafiles_video', models.BigIntegerField(null=True, verbose_name='Видеофильмы', blank=True)),
                ('mediafiles_audio', models.BigIntegerField(null=True, verbose_name='Аудиозаписи', blank=True)),
                ('provided_services', models.TextField(null=True, verbose_name='Услуги, оказываемые библиотекой', blank=True)),
                ('using_rules', models.TextField(null=True, verbose_name='Правила пользования библиотекой', blank=True)),
                ('shedule_mon_from', models.TextField(null=True, verbose_name='Режим работы с - Понедельник', blank=True)),
                ('shedule_mon_to', models.TextField(null=True, verbose_name='Режим работы по - Понедельник', blank=True)),
                ('shedule_tue_from', models.TextField(null=True, verbose_name='Режим работы с - Вторник', blank=True)),
                ('shedule_tue_to', models.TextField(null=True, verbose_name='Режим работы по - Вторник', blank=True)),
                ('shedule_wed_from', models.TextField(null=True, verbose_name='Режим работы с - Среда', blank=True)),
                ('shedule_wed_to', models.TextField(null=True, verbose_name='Режим работы по - Среда', blank=True)),
                ('shedule_thu_from', models.TextField(null=True, verbose_name='Режим работы с - Четверг', blank=True)),
                ('shedule_thu_to', models.TextField(null=True, verbose_name='Режим работы по - Четверг', blank=True)),
                ('shedule_fri_from', models.TextField(null=True, verbose_name='Режим работы с - Пятница', blank=True)),
                ('shedule_fri_to', models.TextField(null=True, verbose_name='Режим работы по - Пятница', blank=True)),
                ('shedule_sat_from', models.TextField(null=True, verbose_name='Режим работы с - Суббота', blank=True)),
                ('shedule_sat_to', models.TextField(null=True, verbose_name='Режим работы по- Суббота', blank=True)),
                ('shedule_sun_from', models.TextField(null=True, verbose_name='Режим работы с - Воскресенье', blank=True)),
                ('shedule_sun_to', models.TextField(null=True, verbose_name='Режим работы по - Воскресенье', blank=True)),
                ('lunch_hour_from', models.TextField(null=True, verbose_name='Обеденный перерыв с', blank=True)),
                ('lunch_hour_to', models.TextField(null=True, verbose_name='Обеденный перерыв по', blank=True)),
                ('inside_lib_work_from', models.TextField(null=True, verbose_name='Внутрибиблиотечная работа с', blank=True)),
                ('inside_lib_work_to', models.TextField(null=True, verbose_name='Внутрибиблиотечная работа по', blank=True)),
                ('period_id', models.IntegerField(null=True, verbose_name='Период - Санитарные дни', blank=True)),
                ('office_id', models.IntegerField(null=True, verbose_name='Аудидитория', blank=True)),
                ('cleanup_days_link', models.ManyToManyField(to='cleanup_days.LibPassportCleanupDays')),
                ('documents_account', models.ManyToManyField(related_name='documents_account', to='documents.LibPassportDocuments')),
                ('documents_legal', models.ManyToManyField(related_name='documents_legal', to='documents.LibPassportDocuments')),
            ],
            options={
                'db_table': 'library_passport',
                'verbose_name': 'Паспорт библиотеки',
                'verbose_name_plural': 'Паспорт библиотеки',
            },
        ),
    ]
