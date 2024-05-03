# pylint: disable=too-many-locals, protected-access, consider-using-f-string, use-dict-literal, too-many-branches
# pylint: disable=too-many-statements, no-else-continue
import re

from django.db import (
    transaction,
)
from eduimporter.XLSReader import (
    DateCell,
    EnumCell,
    IntCell,
    MaybeStringCell,
    StringCell,
    XLSLoader,
)

from .models import (
    Reader,
    RoleTypeEnumerate,
    TrueFalseEnumerate,
)


class _Loader(XLSLoader):
    config = {
        'Читатель': {
            'role': ('Роль в системе', EnumCell(
                choices=RoleTypeEnumerate.get_choices())),
            'reader_user': {
                'fio__iexact': ('ФИО', StringCell()),
                'person__date_of_birth': (
                    'Дата рождения читателя', DateCell()),
            },
            'number': ('Номер читательского билета', StringCell()),
            'year': ('Год, с которого читатель состоит в библиотеке',
                     IntCell()),
            'other_libs': ('Посещение других библиотек', MaybeStringCell()),
            'favorite_subject': ('Любимый предмет в школе', MaybeStringCell()),
            'circles': ('В каких кружках состоит', MaybeStringCell()),
            'reading_about': ('О чем любит читать', MaybeStringCell()),
            'hobby': ('Любимое занятие в свободное время', MaybeStringCell()),
            'is_read': ('Умеет ли читать сам', EnumCell(
                choices=TrueFalseEnumerate.get_choices(), default=None
            )),
            'tech': ('Техника чтения', MaybeStringCell()),
        }
    }


class SafeDict():
    """
    Просто обертка словаря с default=None
    """
    def __init__(self, dic):
        self._dic = dic

    def __getitem__(self, key):
        return self._dic.get(key, None)


def remove_extra_spaces(fio):
    return re.sub(r'\s+', ' ', fio).strip() if fio else None


def import_libreaders(memory_mapped_file, file_name, school_id,
                      caches=None, validate=lambda x: None):
    """
    Импорт классов из XLS
    validate - внешний валидатор строки row.
    Принимает либо None, если все ок, либо месседж с ошибкой
    """

    if caches is None:
        caches = {}

    loader = _Loader(memory_mapped_file)

    def make_log(log):
        return r'\n'.join(
            loader.log +
            loader.prepare_row_errors(log)
        )

    # парсинг файла
    if not loader.load():
        return make_log(loader.rows_log)

    # копия лога для дальнейшего возможного дополнения
    import_log = loader.rows_log

    # кэши
    schoolchild, teacher = [caches.get(k)() for k in (
        'schoolchild', 'teacher')]

    def maybe_get(log, cache, error_msg, multiple_msg, **kwargs):
        try:
            obj = cache.get(**kwargs)
            if not obj:
                log.append(error_msg)
        except cache._model.MultipleObjectsReturned:
            log.append(multiple_msg)
            obj = None
        return obj

    def get_school(**kwargs):
        return maybe_get(
            errors, caches['school'],
            'Организация не найдена',
            'Невозможно однозначно определить организацию',
            **kwargs
        )

    def get_reader(row, obj, params):
        return maybe_get(
            errors,
            obj,
            'Читатель %s %s, %s не найден в системе!' % (
                RoleTypeEnumerate.values[row['role']],
                row['reader_user']['fio__iexact'],
                row['reader_user']['person__date_of_birth']
            ),
            'Невозможно однозначно определить пользователя: '
            '%s %s, %s!' % (
                RoleTypeEnumerate.values[row['role']],
                row['reader_user']['fio__iexact'],
                row['reader_user']['person__date_of_birth']
            ),
            **params['reader_user'])

    school = get_school(id=school_id)

    for sheet in list(loader.data.values()):

        for row in sheet:

            validation_error_list = validate(row)
            if validation_error_list:
                import_log.setdefault(row.get('__xls_pos__'), validation_error_list)
                continue

            row['reader_user']['fio__iexact'] = remove_extra_spaces(
                row['reader_user']['fio__iexact']
            )

            row = SafeDict(row)

            errors = []
            params = {'reader_user': {}}

            schoolchild_id = None
            teacher_id = None
            if row['role'] == RoleTypeEnumerate.STUDENT:
                params['reader_user'] = row['reader_user']
                params['reader_user']['school'] = school
                params['reader_user']['graduated'] = False

                schoolchild_id = get_reader(row, schoolchild, params)
            elif row['role'] == RoleTypeEnumerate.TEACHER:
                params['reader_user'] = row['reader_user']
                params['reader_user']['school'] = school

                teacher_id = get_reader(row, teacher, params)
            else:
                errors.append('Некорректно указана роль')

            if errors:
                import_log.setdefault(row[loader.XLS_POS], []).extend(errors)
                continue

            with transaction.atomic():
                params = dict(
                    schoolchild_id=schoolchild_id.id if schoolchild_id else None,
                    teacher_id=teacher_id.id if teacher_id else None,
                )
                readers = Reader.objects.filter(**params)
                if readers.exists():
                    import_log.setdefault(
                        row[loader.XLS_POS],
                        []
                    ).extend(['Данное физ. лицо уже является '
                              'читателем библиотеки!'])
                    continue
                else:  # pylint: disable=no-else-continue
                    params.update(dict(
                        role=row['role'],
                        number=row['number'],
                        year=row['year'],
                    ))
                    reader = Reader(**params)

                # Проверяем уникальность номера читательского билета
                readers = Reader.objects.filter(
                    number=row['number'],
                    school_id=school_id
                )
                if readers.exists():
                    import_log.setdefault(
                        row[loader.XLS_POS],
                        []
                    ).extend(['Читатель с таким номером читательского билета '
                              'уже зарегистрирован в системе!'])
                    continue

                # Пытаемся проверить любимый предмет по справочнику "Предметы"
                if row['favorite_subject']:

                    discipline_not_found = (
                        'Некорректно указано наименование предмета '
                        '(наименование предмета должно соответствовать '
                        'наименованию предмета в Системе, в справочнике '
                        '"Предметы")'
                    )

                    discipline = maybe_get(
                        errors, caches['discipline'],
                        discipline_not_found, discipline_not_found
                    )
                    if discipline is None:
                        import_log.setdefault(
                            row[loader.XLS_POS],
                            []
                        ).extend([discipline_not_found])

                reader.other_libs = row['other_libs']
                reader.favorite_subject = row['favorite_subject']
                reader.circles = row['circles']
                reader.reading_about = row['reading_about']
                reader.hobby = row['hobby']
                if schoolchild_id:
                    if reader.actual_classyear.study_level.index == 1:
                        reader.is_read = row['is_read']
                    if reader.actual_classyear.study_level.index <= 4:
                        reader.tech = row['tech']
                reader.save()

    return make_log(import_log) or 'Файл успешно импортирован'
