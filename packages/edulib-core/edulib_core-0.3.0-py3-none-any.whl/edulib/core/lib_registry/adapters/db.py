import re

from _collections import (
    defaultdict,
)
from django.db.models import (
    Q,
)
from django.db.models.expressions import (
    Exists,
    Func,
    OuterRef,
    Value,
)
from django.db.models.functions.text import (
    Upper,
)

from edulib.core.adapters.db import (
    AbstractRepository,
)
from edulib.core.lib_authors.models import (
    LibAuthorsRegEntries,
)
from edulib.core.lib_registry.models import (
    LibRegistryEntry,
)

from ..models import (
    LibExchangeFund,
)


class ExchangeFundRepository(AbstractRepository):

    model = LibExchangeFund


exchange_fund = ExchangeFundRepository()


class RegistryEntryRepository(AbstractRepository):

    model = LibRegistryEntry

    def is_unique_in_school(self, entry, school_id, authors_ids):
        """Проверяет уникальность элемента библиотечного реестра."""
        obj_type_id = entry.type.id
        obj_book_title = strip_str(entry.book_title).upper()

        # Отберём только те карточки учета, куда входят авторы
        if authors_ids:
            regentries_ids = LibAuthorsRegEntries.objects.filter(
                author_id__in=authors_ids
            ).values_list('reg_entry', flat=True)
            authors_filter = Q(id__in=regentries_ids)
        else:
            # если авторов нет, то отберем карточки без авторов
            regentries_ids = LibAuthorsRegEntries.objects.filter(
                reg_entry__school_id=school_id,
            ).values_list('author', flat=True)
            authors_filter = ~Q(id__in=regentries_ids)

        # Ищем экземпляры реестра в этой школе такого же типа с такими же авторами
        entries = LibRegistryEntry.objects.annotate(
            btu=Func(Upper('book_title'), Value(' '), Value(''), function='replace')
        ).filter(
            authors_filter,
            school_id=school_id,
            type_id=obj_type_id,
            btu=obj_book_title,
        ).values('btu', 'libauthorsregentries__author_id')
        # При редактировании исключаем себя
        if entry.id:
            entries = entries.exclude(id=entry.id)
        unique = True
        # Сформируем из отобранных экземпляров словарь: ключ - обработанное
        # название, значение - список авторов
        book_authors = defaultdict(set)
        for e in entries:
            book_authors[e['btu']].add(
                e['libauthorsregentries__author_id'])
        # Если при совпадающих названиях совпадают авторы, то
        # уникальность не выполняется. Преобразуем списки авторов
        # в множество, чтобы не учитывать порядок следования.
        if not authors_ids:
            unique = obj_book_title not in book_authors
        else:
            unique = set(authors_ids) != book_authors[obj_book_title]
        return unique

    def get_school_entries_not_in_fund(self, school_id):
        """Карточки учета экземпляров книг, принадлежащих школе и которые не находятся в книгообменном фонде."""

        exchange_fund_subquery = LibExchangeFund.objects.filter(
            lib_reg_entry_id=OuterRef('pk'),
        )

        entries = LibRegistryEntry.objects.filter(
            school_id=school_id
        ).annotate(exchange_exists=Exists(exchange_fund_subquery)).filter(
            exchange_exists=False
        )

        return entries


registry_entries = RegistryEntryRepository()


def strip_str(s):
    """Убирает из строки пробелы и кавычки. Нужна для сравнения."""
    return re.sub(r'''["' ]''', r'', s) if s else ''
