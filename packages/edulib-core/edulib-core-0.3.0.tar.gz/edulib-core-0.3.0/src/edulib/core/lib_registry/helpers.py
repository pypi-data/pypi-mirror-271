"""Вспомогательные функции библиотечного реестра."""
# pylint: disable=no-else-return, consider-using-f-string, too-many-return-statements
import datetime
from collections import (
    defaultdict,
)
from typing import (
    Dict,
)

from django.conf import (
    settings,
)
from django.db import (
    connection as default_connection,
)
from django.db.models import (
    Q,
    QuerySet,
)
from django.template.defaultfilters import (
    safe,
)

from edulib.core.issuance_delivery.models import (
    IssuanceDelivery,
)
from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)
from edulib.core.lib_registry.enums import (
    DefaultSectionsBBC,
    WriteoffReasonEnum,
)
from edulib.core.lib_registry.models import (
    LibRegistryExample,
    LibSummaryBook,
    LibSummaryBookDisposalWriteoffReasons,
)


def make_duration_filter(s):
    try:
        if s.startswith('<='):
            return Q(duration__lte=int(s[2:]))
        elif s.startswith('>='):
            return Q(duration__gte=int(s[2:]))
        elif s.startswith('<'):
            return Q(duration__lt=int(s[1:]))
        elif s.startswith('>'):
            return Q(duration__gt=int(s[1:]))
        elif s.startswith('='):
            return Q(duration=int(s[1:]))
        else:
            return Q(duration__icontains=s)
    except ValueError:
        return Q(duration__icontains=s)


def get_types():
    """Возвращает идентификаторы и названия типов библиотечного реестра."""
    return LibraryExampleType.objects.values_list('pk', 'name').order_by('pk')


def get_date_for_grid(dt):
    """Возвращает дату строкой для правильной сортировки в гриде.

    :param date dt: дата
    """
    return safe(
        '<span style="display:none">%s</span>%s' % (
            datetime.datetime.strftime(dt, '%Y-%m-%d'),
            datetime.datetime.strftime(dt, settings.DATE_FORMAT),
        )
    ) if dt else ''


def get_message_for_issuance_delivery_ids(example_ids):
    """Возвращает сообщение с экземплярами, выданными читателям
    или утерянные

    :param example_ids int_list: список экзмепляров
    """

    issuance_deliveries = IssuanceDelivery.objects.filter(
        Q(
            Q(fact_delivery_date__isnull=True) |
            Q(fact_delivery_date__gt=datetime.date.today())
        ),
        example_id__in=example_ids,
        example__writeoff_date__isnull=True,
    ).values_list(
        'example__card_number', 'example__inv_number'
    )

    writeoff_examples = LibRegistryExample.objects.filter(
        id__in=example_ids,
        writeoff_date__isnull=False,
    ).values_list(
        'card_number', 'inv_number', 'writeoff_reason'
    )

    issuance_delivery_ids = []
    writeoff_examples_ids = defaultdict(list)
    message = ''

    # Занятые экземпляры
    for card_number, inv_number in issuance_deliveries:
        number = card_number or inv_number
        if number:
            issuance_delivery_ids.append(number)

    if issuance_delivery_ids:
        message = (
            'Читателю выданы экземпляры с карточками учета:'
            ' {}.'.format(', '.join(issuance_delivery_ids))
        )

    # Списанные экземпляры
    for card_number, inv_number, reason in writeoff_examples:
        number = card_number or inv_number
        if number:
            writeoff_examples_ids[reason].append(number)

    if writeoff_examples_ids:
        for reason in writeoff_examples_ids:
            # Если указана причина списания, укажем её в сообщении
            writeoff_reason_name = 'Списаны по причине {}'.format(
                WriteoffReasonEnum.values[reason].lower()
            ) if reason else 'Списаны'

            writeoff_message = (
                '{} экземпляры с карточками учета: {}.'.format(
                    writeoff_reason_name,
                    ', '.join(writeoff_examples_ids[reason])
                )
            )
            message = '</br>'.join(filter(bool, [message, writeoff_message]))

    return message


def delete_lib_summary_book_without_examples(school_id, connection=None):
    """Удаление книг поступлений LibSummaryBook в ОО school_id.

    Для которых нет записей в LibRegistryExample (т.е. нет поступлений).
    """
    sql = """
        with exist_records as (
            select distinct on (
                lib_reg_examples.inflow_date, lib_registry.source_id
            ) lib_reg_examples.inflow_date, lib_registry.source_id
            from lib_reg_examples
            join lib_registry
                on lib_registry.id = lib_reg_examples.lib_reg_entry_id
            left join library_source
                on library_source.id = lib_registry.source_id
            where lib_registry.school_id = %(school_id)s
        )
        select id from lib_summary_book
        where lib_summary_book.school_id = %(school_id)s
        and lib_summary_book.id not in (
            select lib_summary_book.id
            from lib_summary_book
            join exist_records
            on exist_records.inflow_date = lib_summary_book.record_date
                and (
                    lib_summary_book.source_id = exist_records.source_id
                    or lib_summary_book.source_id is null
                        and exist_records.source_id is null)
        );
    """
    if connection is None:
        connection = default_connection

    with connection.cursor() as cursor:
        cursor.execute(sql, {'school_id': school_id})
        result = cursor.fetchall()

    LibSummaryBook.objects.filter(id__in=[r[0] for r in result]).delete()


def calc_writeoff_reasons(lsb):
    """Подсчет документов по причинам списания.

    :param lsb LibSummaryBookDisposal(): экземпляр выбытия КСУ.
    """
    for reason, books_count in (
            lsb.get_examples_writeoff_reason_count().items()):
        lsb_wr = LibSummaryBookDisposalWriteoffReasons.objects.filter(
            lib_summary_book_id=lsb.id,
            writeoff_reason=reason,
        ).first()
        if not lsb_wr:
            lsb_wr = LibSummaryBookDisposalWriteoffReasons()
            lsb_wr.lib_summary_book_id = lsb.id
            lsb_wr.writeoff_reason = reason
        lsb_wr.books_count = books_count
        lsb_wr.save()


def get_default_bbc_counts(bbc_count_query: QuerySet) -> Dict[int, int]:
    """Расчет количества книг по ББК в соответствии с разделами по умолчанию."""
    bbc_id_counts = defaultdict(int)
    # Определяем дефолтные секции расчета ББК
    q_filteres = Q()
    # Формируем фильтр для получения количества книг ББК по индексам секций
    for section in DefaultSectionsBBC.values.values():
        section_q_filter = Q()
        for bbc_index in section.get('bbc_indexes'):
            section_q_filter |= Q(bbc__index_bbc__startswith=bbc_index)
        q_filteres |= section_q_filter

    bbc_count_query = bbc_count_query.filter(
        q_filteres
    ).values_list(
        'bbc__index_bbc',
        'books_count',
    )
    for key, section in DefaultSectionsBBC.values.items():
        section_indexes = section['bbc_indexes']
        section_indexes_exclude = section['bbc_indexes_exclude']
        bbc_id_counts[key] = 0
        for bbc_index, bbc_count_books in bbc_count_query:
            # Если индекс из БД начинается хотя бы на один из индексов секции
            if any(bbc_index.startswith(str(section_index)) for section_index in section_indexes):
                # Если есть индексы, которые необходимо исключить по правилу
                if not (
                    any(
                        bbc_index.startswith(
                            str(section_index)
                        ) for section_index in section_indexes_exclude
                    )
                ):
                    bbc_id_counts[key] += bbc_count_books

    return bbc_id_counts
