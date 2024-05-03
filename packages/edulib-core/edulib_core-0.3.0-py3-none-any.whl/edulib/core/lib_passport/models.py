"""Паспорт библиотеки. Модели."""
from django.db import (
    models,
)

from edulib.core import (
    domain,
)
from edulib.core.address.services.validators import (
    addr_field_validator,
    corps_validator,
    house_validator,
)
from edulib.core.base.models import (
    BaseModel,
)
from edulib.core.lib_passport.cleanup_days.models import (
    LibPassportCleanupDays,
)
from edulib.core.lib_passport.documents.models import (
    LibPassportDocuments,
)


class LibPassport(BaseModel):
    """Паспорт библиотеки."""

    audit_log = True  # Включение логирования для этой модели

    school_id = models.IntegerField(verbose_name='id школы', unique=True)

    name = models.CharField(max_length=250, verbose_name='Наименование')
    date_found_month = models.SmallIntegerField(
        verbose_name='Дата основания (месяц)',
        choices=domain.MonthEnum.get_choices(),
        default=1
    )
    date_found_year = models.PositiveSmallIntegerField(
        verbose_name='Дата основания (год)',
        null=True,
        blank=True
    )
    library_chief_id = models.IntegerField(
        verbose_name='Зав. библиотеки',
        null=True,
        blank=True
    )

    # Вкладка "Контактная информация"
    is_address_match = models.BooleanField(
        verbose_name='Адрес совпадает с адресом ОО', default=False
    )
    f_address_place = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        validators=[addr_field_validator],
        verbose_name='Населенный пункт'
    )
    f_address_street = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        validators=[addr_field_validator],
        verbose_name='Улица'
    )
    f_address_house = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[house_validator],
    )
    f_address_house_guid = models.CharField(
        max_length=36,
        null=True,
        blank=True,
        validators=[addr_field_validator],
        verbose_name='Дом'
    )
    f_address_corps = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        validators=[corps_validator],
        verbose_name='Корпус'
    )
    f_address_full = models.CharField(max_length=200, null=True, blank=True)
    f_address_zipcode = models.CharField(max_length=10, null=True, blank=True)

    is_telephone_match = models.BooleanField(
        verbose_name='Телефон совпадает с телефоном ОО', default=False
    )
    telephone = models.CharField(max_length=50, null=True, blank=True)

    is_email_match = models.BooleanField(
        verbose_name='Email совпадает с email ОО', default=False
    )
    email = models.CharField(max_length=50, null=True, blank=True)

    # Вкладка "Материальная база"
    is_abonement = models.BooleanField(
        verbose_name='Абонемент', default=True
    )
    is_reading_room = models.BooleanField(
        verbose_name='Читальный зал', default=True
    )

    reading_room_type = models.PositiveIntegerField(
        'Тип читальногой зала',
        choices=domain.ReadingRoomTypeEnum.get_choices(),
        null=True, blank=True
    )

    is_lib_store = models.BooleanField(
        verbose_name='Книгохранилище',
        default=True
    )
    book_fund = models.BigIntegerField(
        verbose_name='Книжный фонд (экз.)',
        null=True, blank=True
    )
    schoolbook_fund = models.BigIntegerField(
        verbose_name='Учебники (экз.)',
        null=True, blank=True
    )
    main_fund = models.BigIntegerField(
        verbose_name='Основной фонд (экз.)',
        null=True, blank=True
    )

    is_media = models.BooleanField(
        verbose_name='Медиатека', default=False
    )
    is_pc_base = models.BooleanField(
        verbose_name='На базе компьютерного класса', default=False
    )

    media_pc_cnt = models.BigIntegerField(
        verbose_name='Кол-во компьютеров для пользования медиатекой',
        null=True, blank=True
    )
    is_access_internet = models.BooleanField(
        verbose_name='Доступ в сеть Интернет', default=False
    )
    mediafiles_total = models.BigIntegerField(
        verbose_name='Медиафайлы (экз.)', null=True, blank=True
    )
    mediafiles_video = models.BigIntegerField(
        verbose_name='Видеофильмы', null=True, blank=True
    )
    mediafiles_audio = models.BigIntegerField(
        verbose_name='Аудиозаписи', null=True, blank=True
    )

    # Вкладка "Дополнительная информация"
    provided_services = models.TextField(
        verbose_name='Услуги, оказываемые библиотекой',
        null=True, blank=True
    )
    using_rules = models.TextField(
        verbose_name='Правила пользования библиотекой',
        null=True, blank=True
    )

    # Режим работы
    shedule_mon_from = models.TextField(
        verbose_name='Режим работы с - Понедельник', null=True, blank=True
    )
    shedule_mon_to = models.TextField(
        verbose_name='Режим работы по - Понедельник', null=True, blank=True
    )
    shedule_tue_from = models.TextField(
        verbose_name='Режим работы с - Вторник', null=True, blank=True
    )
    shedule_tue_to = models.TextField(
        verbose_name='Режим работы по - Вторник', null=True, blank=True
    )
    shedule_wed_from = models.TextField(
        verbose_name='Режим работы с - Среда', null=True, blank=True
    )
    shedule_wed_to = models.TextField(
        verbose_name='Режим работы по - Среда', null=True, blank=True
    )
    shedule_thu_from = models.TextField(
        verbose_name='Режим работы с - Четверг', null=True, blank=True
    )
    shedule_thu_to = models.TextField(
        verbose_name='Режим работы по - Четверг', null=True, blank=True
    )
    shedule_fri_from = models.TextField(
        verbose_name='Режим работы с - Пятница', null=True, blank=True
    )
    shedule_fri_to = models.TextField(
        verbose_name='Режим работы по - Пятница', null=True, blank=True
    )
    shedule_sat_from = models.TextField(
        verbose_name='Режим работы с - Суббота', null=True, blank=True
    )
    shedule_sat_to = models.TextField(
        verbose_name='Режим работы по- Суббота', null=True, blank=True
    )
    shedule_sun_from = models.TextField(
        verbose_name='Режим работы с - Воскресенье', null=True, blank=True
    )
    shedule_sun_to = models.TextField(
        verbose_name='Режим работы по - Воскресенье', null=True, blank=True
    )

    # Обеденный перерыв
    lunch_hour_from = models.TextField(
        verbose_name='Обеденный перерыв с', null=True, blank=True
    )
    lunch_hour_to = models.TextField(
        verbose_name='Обеденный перерыв по', null=True, blank=True
    )

    # Внутрибиблиотечная работа
    inside_lib_work_from = models.TextField(
        verbose_name='Внутрибиблиотечная работа с', null=True, blank=True
    )
    inside_lib_work_to = models.TextField(
        verbose_name='Внутрибиблиотечная работа по', null=True, blank=True
    )

    # Санитарные дни
    period_id = models.IntegerField(
        verbose_name='Период - Санитарные дни', null=True, blank=True
    )

    cleanup_days_link = models.ManyToManyField(LibPassportCleanupDays)

    # Вкладка "Документы"
    documents_legal = models.ManyToManyField(
        LibPassportDocuments,
        related_name='documents_legal'
    )
    documents_account = models.ManyToManyField(
        LibPassportDocuments,
        related_name='documents_account'
    )

    # Вкладка "Инвентарь"
    office_id = models.BigIntegerField(
        unique=True,
        verbose_name='Аудитория',
        null=True,
        help_text='ID аудитории'
    )

    class Meta:
        db_table = 'library_passport'
        verbose_name = 'Паспорт библиотеки'
        verbose_name_plural = 'Паспорт библиотеки'

    def __str__(self):
        """Строковое представление объекта."""
        # pylint: disable=invalid-str-returned
        return self.name

    def save(self, *args, **kwargs):
        # Валидация полей модели
        self.full_clean()
        super().save(*args, **kwargs)
