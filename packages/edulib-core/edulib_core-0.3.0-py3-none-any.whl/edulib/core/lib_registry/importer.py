# pylint: disable=too-many-locals, protected-access, consider-using-f-string, consider-iterating-dictionary
# pylint: disable=redefined-builtin, use-dict-literal
import re
from decimal import (
    Decimal,
)

import eduimporter as importer
from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError,
)
from django.db import (
    IntegrityError,
    transaction,
)
from xlrd import (
    XLRDError,
)

from edulib.core.lib_authors.models import (
    LibAuthorsRegEntries,
    LibraryAuthors,
)

from . import (
    models,
)


initials_re = r'\b(\w\s*\.\s*(?:\w\s*\.)?)'


class PositiveIntCell(importer.IntCell):
    """
    Ячейка, содержащая число больше 0
    """
    def _parse(self, value):
        result, _ = super()._parse(value)
        if result <= 0:
            raise importer.CellValueError(
                f'Число должно быть больше нуля! "{result}"'
            )
        return self.result(result)


class _Loader(importer.XLSLoader):
    config = {
        'Экземпляр': {
            'type': ('Тип', importer.StringCell()),
            'book_title': ('Заглавие', importer.StringCell()),
            'authors': ('Автор (-ы)', importer.StringCell()),
            'udc': ('Раздел УДК', importer.MaybeStringCell()),
            'study_levels': ('Параллель', importer.MaybeStringCell()),
            'subject': ('Предмет', importer.MaybeStringCell()),
            'tags': ('Ключевые слова', importer.MaybeStringCell()),
            'short_info': ('Краткое описание', importer.MaybeStringCell()),
            'inv_number': ('Инвентарный номер / номер карточки учета',
                           importer.StringCell()),
            'inflow_date': ('Дата поступления единицы экземпляра',
                            importer.DateCell()),
            'edition': ('Издание', importer.MaybeStringCell()),
            'edition_place': ('Место издания', importer.StringCell()),
            'pub_office': ('Издательство', importer.StringCell()),
            'edition_year': ('Год издания', importer.IntCell()),
            'book_code': ('Шифр книги', importer.StringCell()),
            'duration': ('Кол-во страниц/ длительность', PositiveIntCell()),
            'max_date': ('Максимальный срок выдачи (в днях)',
                         importer.MaybeIntCell()),
            'price': ('Стоимость экземпляра (в рублях)',
                      importer.MaybeRawCell()),
        }
    }


class SafeDict:
    """
    Просто обертка словаря с default=None
    """
    def __init__(self, dic):
        self._dic = dic

    def __getitem__(self, key):
        return self._dic.get(key, None)


def import_libregistry(memory_mapped_file, file_name, school_id, caches=None,
                       validate=lambda x: None):
    """
    Импорт классов из XLS
    validate - внешний валидатор строки row.
    Принимает либо None, если все ок, либо месседж с ошибкой
    """

    if caches is None:
        caches = {}

    try:
        loader = _Loader(memory_mapped_file)
    except XLRDError as exc:
        raise ValidationError('Неверный формат файла.') from exc

    def make_log(log):
        return r'\n'.join(
            loader.log +
            loader.prepare_row_errors(log)
        )

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

    school = get_school(id=school_id)
    try:
        ministry = school.get_ministry()
    except ObjectDoesNotExist:
        ministry = None

    # парсинг файла
    if not loader.load():
        return make_log(loader.rows_log)

    # копия лога для дальнейшего возможного дополнения
    import_log = loader.rows_log

    errors = []
    for sheet_index, (sheet_name, sheet_values) in enumerate(
            list(loader.data.items()), 1):

        # Начинаем нумерацию с 2, т.к. первая строка - заголовок таблицы
        for row_index, row in enumerate(sheet_values, 2):

            validation_error_list = validate(row)
            if validation_error_list:
                import_log.setdefault(row.get('__xls_pos__'),
                                      validation_error_list)
                continue

            row = SafeDict(row)

            location = {
                'sheet_name': sheet_name,
                'sheet_index': sheet_index,
                'row_index': row_index,
            }

            entry_data = parse_regentry_info(
                row, errors, caches, school, ministry)

            is_classbook = (
                getattr(entry_data, 'type', None) and
                entry_data.type.id == models.LibraryExampleType.CLASSBOOK_ID
            )

            example_data, example_additional_data = parse_example_info(
                row, is_classbook, errors, caches, school)

            if errors:
                import_log.setdefault(row[loader.XLS_POS], []).extend(errors)
                continue

            # Сравниваем распарсенное с содержимым библиотечного реестра
            with transaction.atomic():

                entry = get_or_create_entry(entry_data, location)
                example = get_or_create_example(
                    entry, example_data, example_additional_data, is_classbook)

                try:
                    example.save()
                except IntegrityError as exc:
                    raise ValidationError(
                        'ЛИСТ "{sheet_name}" ({sheet_index}), строка '
                        '{row_index}: Ошибка сохранения экземпляра книги. '
                        'Проверьте корректность данных.'.format(**location)
                    ) from exc
                except ValidationError as e:
                    errors.append(e.message)
                    import_log.setdefault(row[loader.XLS_POS], []).extend(
                        errors)

    if errors:
        message = 'При импорте файла произошла ошибка(и).\n'
        message += make_log(import_log)
    else:
        message = 'Файл успешно импортирован'
    return message


def get_or_create_entry(entry_data, error_location):

    authors_names = parse_authors_string(entry_data.authors)

    # Попробуем найти подходящую карточку учета (по названию и авторам)
    candidate_entries = models.LibRegistryEntry.objects.filter(
        school_id=entry_data.school_id,
        type=entry_data.type,
        book_title__smart_iexact=entry_data.book_title,
    )
    if len(candidate_entries) > 1:
        candidate_entries = candidate_entries.filter(
            book_title=entry_data.book_title)
    for candidate_entry in candidate_entries:
        lib_authors_names = LibAuthorsRegEntries.objects.filter(
            reg_entry=candidate_entry
        ).values_list('author__name', flat=True)
        if (len(authors_names) == len(lib_authors_names) and
                not _new_authors(authors_names, lib_authors_names)):
            return candidate_entry

    # Если не нашли, используем еще не сохраненную entry_data
    entry = entry_data
    entry.authors = '-'  # устаревшее поле для списка авторов

    # Добавляем авторов, если нужно
    authors_to_link = []
    for author_name in authors_names:
        possible_authors = LibraryAuthors.objects.filter(
            name__smart_icontains=crop_initials(author_name),
        )
        for possible_author in possible_authors:
            if not _new_authors((author_name, ), (possible_author.name,)):
                authors_to_link.append(possible_author)
                break
        else:
            new_author = LibraryAuthors(name=canonical_form(author_name))
            authors_to_link.append(new_author)

    # Сохраняем карточку, авторов и связи
    try:
        entry.save()
        for author in authors_to_link:
            if author.id is None:
                author.save()
            link = LibAuthorsRegEntries(author=author, reg_entry=entry)
            link.save()
        # Сохраняем уровни обучения:
        if entry_data._study_levels:
            entry.study_levels.set(entry_data._study_levels)
    except IntegrityError as exc:
        raise ValidationError(
            'ЛИСТ "{sheet_name}" ({sheet_index}), строка '
            '{row_index}: Ошибка сохранения карточки учета. '
            'Проверьте корректность данных.'.format(**error_location)
        ) from exc
    return entry


def parse_authors_string(authors_string):
    """Список имен без запятой в качестве разделителя инициалов или авторов"""
    # Одного автора иногда записывают в виде 'Пушкин, А.С.' или 'Пушкин, А.'
    _, end_initials_count = re.subn(
        r',\s*' + initials_re + r'\s*$', '', authors_string, flags=re.U)
    _, initials_count = re.subn(initials_re, '', authors_string, flags=re.U)
    commas_count = authors_string.count(',')
    list_of_names = None
    if end_initials_count == 1:
        list_of_names = [authors_string.replace(',', '')]
    # Если строка вроде 'Vonnegut, Jr. Kurt ' и она уже есть в системе
    elif commas_count == 1 and initials_count == 0:
        authors_with_comma = LibraryAuthors.objects.filter(
            name__contains=','
        ).values_list('name', flat=True)
        if not _new_authors((authors_string,), authors_with_comma):
            list_of_names = [authors_string]
    if list_of_names is None:
        list_of_names = authors_string.split(',')
    return list_of_names


def _new_authors(input_names, stored_names):
    """
    Сравнивает авторов, игнорируя порядок имен, фамилий, слов мл. и т.п.

    Возвращает список имен авторов input_names, для которых не нашлось
    соответствия в stored_names.
    """

    stored_forms = set(map(comparsion_form, stored_names))
    return [name for name in input_names
            if comparsion_form(name) not in stored_forms]


def canonical_form(author_name):
    """Переносит инициалы в конец имени, удаляя лишние пробелы"""
    # А. С. Пушкин -> Пушкин А.С.
    second_name, initials = _split_author_name(author_name)
    if initials:
        return ' '.join([second_name, initials])
    return second_name


def crop_initials(author_name):
    rest_of_the_name, _ = _split_author_name(author_name)
    return rest_of_the_name


def _split_author_name(author_name):
    # 'А. С. Пушкин' -> ('Пушкин', 'А.С.')
    initials = re.findall(initials_re, author_name, flags=re.U)
    if not initials:
        return author_name.strip(), None
    rest_of_the_name = re.sub(initials_re, '', author_name, flags=re.U)
    rest_of_the_name = re.sub(r'\s+', ' ', rest_of_the_name.strip(), flags=re.U)
    initials = re.sub(r'\s*', '', initials[0], flags=re.U)
    return rest_of_the_name, initials


def comparsion_form(author_name):
    # Б.Л.ван дер Варден -> ван варден дер б.л.
    lower_form = canonical_form(author_name).lower()
    diacritical_free_form = re.sub('ё', 'е', lower_form, flags=re.U)
    punctuationless_form = re.sub(r'[^\w .]', '', diacritical_free_form,
                                  flags=re.U)
    return ' '.join(sorted(punctuationless_form.split()))


def smart_maybe_get(log, cache, error_msg, multiple_msg, **lookups):
    """
    Обертка для get из django с логированием и сопоставлением Е и Ё

    Если lookups соджит поиск из семейства '__smart' (например,
    name__smart_icontains) и возникает ошибка MultipleObjectsReturned, то
    производится попытка найти единственный объект, заменяя все __smart
    поиски на стандартные (Например, name__icontains)
    """
    try:
        obj = cache.get(**lookups)
        # При рекурсии error_msg is None
        if not obj and (error_msg is not None):
            log.append(error_msg)
    except cache._model.MultipleObjectsReturned:
        if any(['__smart' in list(lookups.keys())]):
            narrowed_lookup = {keyword.replace('__smart', ''): arg for
                               keyword, arg in list(lookups.items())}
            obj = smart_maybe_get(log, cache, None, multiple_msg,
                                  **narrowed_lookup)
        else:
            obj = None
            log.append(multiple_msg)
    return obj


def parse_regentry_info(row, errors, caches, school, ministry):

    entry_data = models.LibRegistryEntry(school_id=school.id)

    type = smart_maybe_get(
        errors, caches['type'],
        'Тип библиотечного экземпляра "%s" не найден в системе! '
        '(наименование типа должно соответствовать наименованию типа '
        'в Системе, в справочнике «Типы библиотечных экземпляров»)' %
        row['type'],
        'Невозможно однозначно определить тип библиотечного '
        'экземпляра: %s!' % row['type'],
        name=row['type']
    )
    if type:
        entry_data.type = type

    entry_data.udc = None
    if row['udc']:
        _udc = re.split('[-–]', row['udc'])

        if len(_udc) == 2:
            udc_code, udc_name = _udc[0].strip(), _udc[1].strip()
            entry_data.udc = smart_maybe_get(
                errors, caches['udc'],
                'Раздел УДК "%s" не найден в системе! '
                '(раздел УДК должен соответствовать разделу УДК в '
                'Системе, в справочнике «Разделы УДК» '
                'по форме: код_раздела – наименование_раздела)' %
                row['udc'],
                'Невозможно однозначно определить раздел УДК: %s!' %
                row['udc'],
                code=udc_code, name__smart_iexact=udc_name
            )
        else:
            errors.append(
                'Некорректный формат раздела УДК: "{0}". Раздел УДК вводится '
                'в формате "код_раздела – наименование_раздела"'.format(
                    row['udc']))

    # Определяем уровни обучения:
    _split_study_levels = (
        row['study_levels'].replace('.', ',').split(',') if row['study_levels']
        else []
    )
    entry_data._study_levels = []
    for lvl in _split_study_levels:
        try:
            study_level = smart_maybe_get(
                errors, caches['study_levels'],
                'Параллель "%s" не найдена в системе! ' % lvl,
                'Невозможно однозначно определить параллель %s!' % lvl,
                index=lvl
            )
        except ValueError:
            errors.append(
                'Столбец "Параллель": Неправильный формат ввода: '
                '"{0}"!'.format(lvl)
            )
            study_level = None
        if study_level:
            entry_data._study_levels.append(study_level.id)

    lib_subject = None
    if row['subject']:
        lib_subject = smart_maybe_get(
            errors, caches['subject'],
            'Наименование предмета "%s" не найдено в системе! '
            '(наименование предмета должно соответствовать '
            'наименованию предмета в Системе, '
            'в справочнике «Предметы»)' %
            row['subject'],
            'Невозможно однозначно определить '
            'наименование предмета: %s!' %
            row['subject'],
            name=row['subject'],
            school__in=(school, ministry)
        )
    entry_data.discipline_id = lib_subject.id if lib_subject else None

    # Дополняем запись карточки доп. данными
    entry_data.book_title = row['book_title'].strip()
    entry_data.tags = row['tags']
    entry_data.short_info = row['short_info']
    entry_data.authors = row['authors']

    return entry_data


def parse_example_info(row, is_classbook, errors, caches, school):

    # Если не учебник
    if not is_classbook:
        # Проверка на уникальность инвентарного номера
        if models.LibRegistryExample.objects.filter(
                inv_number=row['inv_number'],
                lib_reg_entry__school_id=school.id
        ).exists():
            errors.append(
                'Указан неуникальный инвентарный номер для '
                'выбранной организации.'
            )

    lib_publishing = smart_maybe_get(
        errors, caches['pub_office'],
        'Издательство "%s" не найдено в системе! '
        '(наименование издательства должно соответствовать '
        'наименованию типа в Системе, в справочнике «Издательства»)' %
        row['pub_office'],
        'Невозможно однозначно определить издательство '
        'экземпляра: %s!' % row['pub_office'],
        name__smart_iexact=row['pub_office']
    )

    example_data = dict(
        inv_number=row['inv_number'] if not is_classbook else None,
        card_number=row['inv_number'] if is_classbook else None,
        inflow_date=row['inflow_date'],
        edition_place=row['edition_place'],
        publishing=lib_publishing,
        edition_year=row['edition_year'],
        duration=row['duration'],
        book_code=row['book_code']
    )

    example_additional_data = dict(
        edition=row['edition'],
        max_date=row['max_date']
    )

    price_pattern = r'^(?P<price>(\d{1,5}\.\d{1,2})|(\d{1,5}))'
    price_regex = re.compile(price_pattern)
    if row['price']:
        result = price_regex.match(row['price'])
        if result:
            example_additional_data['price'] = Decimal(result.group('price'))

    return example_data, example_additional_data


def get_or_create_example(entry, example_data, example_additional_data,
                          is_classbook):

    params = dict(lib_reg_entry=entry, **example_data)

    if is_classbook:
        # для учебников всегда создаем новые экземпляры при импорте
        example = models.LibRegistryExample(**params)
    else:
        try:
            example = models.LibRegistryExample.objects.get(
                **params)
        except models.LibRegistryExample.DoesNotExist:
            example = models.LibRegistryExample(**params)

    for attr, value in list(example_additional_data.items()):
        setattr(example, attr, value)

    return example
