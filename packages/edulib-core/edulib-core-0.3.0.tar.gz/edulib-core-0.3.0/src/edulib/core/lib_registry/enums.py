"""Перечисления библиотечного реестра."""
from edulib.core.base.domain import (
    BaseEnumerate,
)


class WriteoffReasonEnum(BaseEnumerate):
    """Перечисление причин списания экземпляров библиотечного реестра."""

    OBSOLESCENCE = 1
    LOSS = 2
    SENILITY = 3
    DEFECTIVENESS = 4
    NONRELEVANT = 5

    values = {
        OBSOLESCENCE: 'Устарелость по содержанию',
        LOSS: 'Утрата',
        SENILITY: 'Ветхость',
        DEFECTIVENESS: 'Дефектность',
        NONRELEVANT: 'Непрофильность',
    }


class DefaultSectionsBBC(BaseEnumerate):
    """Разделы ББК для КСУ по умолчанию.

    В рамках разделов определены имена, индексы для фильтрации, а также индексы исключений.
    bbc_indexes - определяют значения, по которым будет вестись фильтрация разделов ББК.
    bbc_indexes_exclude - определяют исключения, которые могут встречаться при поиске,
     но не должны учитывать при расчетах/фильрациях.
    """

    NATURAL_SCIENCE = 1
    POPULAR_SCIENCE = 2
    HUMANITARIAN_SCIENCE = 3
    UNIVERSAL_REFERENCE_LITERATURE = 4
    PEDAGOGICAL_SCIENCES = 5
    ARTS_AND_SPORTS = 6
    FICTION = 7
    SCHOOLBOOK = 8

    values = {
        NATURAL_SCIENCE: {
            'name': 'Естеств. науки (2)',
            'bbc_indexes': (2, ),
            'bbc_indexes_exclude': (),
        },
        POPULAR_SCIENCE: {
            'name': 'Научно-популярная (3,4,5)',
            'bbc_indexes': (3, 4, 5),
            'bbc_indexes_exclude': (),
        },
        HUMANITARIAN_SCIENCE: {
            'name': 'Обществ.-гуманит. науки (6,8)',
            'bbc_indexes': (6, 8),
            'bbc_indexes_exclude': (84, 85),
        },
        UNIVERSAL_REFERENCE_LITERATURE: {
            'name': 'Универс. содерж.и справочная литература (9)',
            'bbc_indexes': (9, ),
            'bbc_indexes_exclude': (),
        },
        PEDAGOGICAL_SCIENCES: {
            'name': 'Педагогич. науки (74)',
            'bbc_indexes': (74, ),
            'bbc_indexes_exclude': (),
        },
        ARTS_AND_SPORTS: {
            'name': 'Искусство и спорт (75, 85)',
            'bbc_indexes': (75, 85),
            'bbc_indexes_exclude': (),
        },
        FICTION: {
            'name': 'Худож. лит. (84)',
            'bbc_indexes': (84, ),
            'bbc_indexes_exclude': (),
        },
        SCHOOLBOOK: {
            'name': 'Учебники',
            'bbc_indexes': ('class_books',),
            'bbc_indexes_exclude': (),
        },
    }
