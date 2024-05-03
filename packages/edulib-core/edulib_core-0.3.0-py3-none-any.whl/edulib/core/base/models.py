# pylint: disable=protected-access, consider-using-f-string
import copy
import datetime
import uuid
from collections import (
    defaultdict,
)
from functools import (
    partial,
)

from django.core.exceptions import (
    ValidationError,
)
from django.db import (
    connections,
    models,
    router,
)
from django.db.models import (
    FileField,
)
from django.db.models.base import (
    Model,
)
from django.db.models.deletion import (
    Collector,
)
from django.db.transaction import (
    on_commit,
)


def get_all_related_objects(model):
    return [
        f for f in model._meta.get_fields()
        if (f.one_to_many or f.one_to_one) and
        f.auto_created and not f.concrete
    ]


def get_unique_code(model):
    """Генерация уникального кода для поля SimpleDictionary.code."""
    while True:
        code = str(uuid.uuid4())[:18]
        if not model.objects.filter(code__iexact=code).exists():
            return code


def safe_delete(model):
    """
    Функция выполняющая "безопасное" удаление записи из БД.

    В случае, если удаление не удалось по причине нарушения целостности,
    то возвращается false. Иначе, true
    к тому же функция пересчитывает MPTT индексы дерева
    т.к. стандартный пересчет запускается при вызове model_instance.delete()
    """
    models.signals.pre_delete.send(sender=model.__class__, instance=model)
    db_alias = router.db_for_write(model.__class__, instance=model)
    try:
        connection = connections[db_alias]
        cursor = connection.cursor()
        sql = "DELETE FROM %s WHERE id = %s" % (
            connection.ops.quote_name(model._meta.db_table), model.id)
        cursor.execute(sql)
    except Exception as e:
        # Встроенный в Django IntegrityError не генерируется.
        # Кидаются исключения, специфичные для каждого драйвера БД.
        # Но по спецификации PEP 249 все они называются IntegrityError
        if e.__class__.__name__ == 'IntegrityError':
            return False
        raise

    # добавим пересчет mptt дерева
    # (т.к. стандартный пересчет вешается на метод self.delete()
    if hasattr(model, '_tree_manager') and callable(
            getattr(model._tree_manager, '_close_gap', None)):
        # это, видимо, mptt модель
        opts = model._meta
        right = getattr(model, getattr(opts, 'right_attr', 'rght'))
        left = getattr(model, getattr(opts, 'left_attr', 'lft'))
        tree = getattr(model, getattr(opts, 'tree_id_attr', 'tree_id'))
        model._tree_manager._close_gap(right - left + 1, right, tree)

    models.signals.post_delete.send(sender=model.__class__, instance=model)
    return True


class BaseModel(Model):
    """
    Базовый класс для всех моделей объектов, подлежащих репликации
    """

    # связь с зависимыми моделями, запрещающая удаление объекта
    # указывается список имен классов
    PROHIBIT_DELETE_RELATIONS = []

    created = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Дата создания'
    )

    modified = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        verbose_name='Дата изменения'
    )

    report_constructor_params = {
        'except': ('created', 'modified')
    }

    def safe_delete(self):
        """
        Функция выполняющая "безопасное" удаление записи из БД.
        В случае, если запись не удалось удалить по причине нарушения
        целостности, возвращается False, иначе True.
        """
        self.delete_filefields()

        if not safe_delete(self):
            raise ValidationError(
                "Объект не может быть удален! Возможно на него есть ссылки."
            )
        return True

    def get_related_objects(self, using=None):
        """
        Возвращает структуру содержащую классы моделей,
        первичные ключи и экземпляры записей, зависящие от текущей записи.
        Возвращаемая структура имеет вид:
        [(КлассМодели1,
            {id1: ЭкземплярМодели1cID1, id2: ЭкземплярМодели1cID2, ...}),
         (КлассМодели2,
            {id1: ЭкземплярМодели2cID1, id2: ЭкземплярМодели2cID2, ...} },
        ...]
        @deprecated: Вытаскивает много данных. Сервер может зависнуть!
        """
        using = using or router.db_for_write(self.__class__, instance=self)
        collector = Collector(using=using)
        collector.collect([self])
        return list(collector.data.items())

    def delete_related(self, affected=None, using=None):
        """
        Стандартное каскадное удаление объектов в django,
        дополненное проверкой на удаляемые классы моделей affected.
        По умолчанию affected содержит пустой список
        - это ограничивает удаляемые модели только текущим классом.
        К перечисленным в affected классам текущий добавляется автоматически.
        Если удаление не удалось выполнить, возвращает False, иначе True.
        Пример:
            Model1.objects.get(id=1).delete_related(affected=[Model2, Model3])
        """
        # Кописаст из django.db.models.Model delete()
        using = using or router.db_for_write(self.__class__, instance=self)
        assert self._get_pk_val() is not None, (
            "%s object can't be deleted because its "
            "%s attribute is set to None."
        ) % (
            self._meta.object_name,
            self._meta.pk.attname
        )

        collector = Collector(using=using)
        collector.collect([self])
        # cut

        affected = affected or []
        assert isinstance(affected, list), (
            'Affected models must be the list type')
        affected.append(self.__class__)

        for model in collector.data.keys():
            if model not in affected:
                return False

        collector.delete()
        return True

    def update(self, dictionary):
        for key, val in dictionary.items():
            setattr(self, key, val)

    def duplicate(self):
        """Получение копии объекта для последующего сохранения"""
        new_self = copy.deepcopy(self)
        # pylint: disable=attribute-defined-outside-init
        new_self.id = None
        new_self.modified, new_self.created = None, None
        return new_self

    @classmethod
    def get_or_new(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            return cls(**kwargs)

    def delete(self, *args, **kwargs):
        """Удаление."""
        self.delete_filefields()
        super().delete(*args, **kwargs)

    def delete_filefields(self):
        """Удаление файлов по файловым полям."""
        def remove_files(file_fields):
            for field in file_fields:
                fieldfile = getattr(self, field.attname)
                fieldfile.delete(save=False)

        on_commit(partial(remove_files, self.get_file_fields()))

    def get_file_fields(self):
        """Файловые поля."""
        return (field for field in self._meta.concrete_fields
                if isinstance(field, FileField))

    def save(self, *args, **kwargs):
        """
        Сохранение объекта.
        """
        exclude_not_null_fields = kwargs.pop('exclude_not_null_fields', None)
        self.field_preparation(exclude_not_null_fields)
        self.add_field_updatable_fields(kwargs)
        super().save(*args, **kwargs)

    def field_preparation(self, exclude_fields=None):  # noqa C901
        """
        Подготовка полей перед сохранением.

        Обрезка концевых пробелов у строковых полей с
        последующим превращением '' в None.
        Преобразование значения в дату, если тип поля DateField.
        """
        if exclude_fields:
            assert isinstance(exclude_fields, (list, tuple))
        for f in self._meta.fields:
            if isinstance(f, (models.TextField, models.CharField)):
                try:
                    val = getattr(self, f.attname)
                except AttributeError:
                    continue
                if isinstance(val, str):
                    val = val.strip()
                    if f.max_length and len(val) > f.max_length:
                        raise ValidationError(
                            'Превышена длина поля "%s"!' % f.verbose_name)
                if exclude_fields is None or f.name not in exclude_fields:
                    val = val or None
                setattr(self, f.attname, val)
            elif isinstance(f, models.DateField):
                try:
                    val = getattr(self, f.attname)
                except AttributeError:
                    continue
                # Оставляем у значения только дату, если тип поля - дата,
                # но не дата-время
                if (isinstance(val, datetime.datetime) and
                        not isinstance(f, models.DateTimeField)):
                    val = val.date()
                val = val or None
                setattr(self, f.attname, val)

    @staticmethod
    def add_field_updatable_fields(kwargs):
        """
        Добавление поля modified в словарь в update_fields.

        Если в словаре передаётся параметр update_modified_field
        со значением False, то поле modified не добавляется в
        словарь update_fields.
        """
        if (
                kwargs.get(
                    'update_modified_field',
                    True
                ) and 'update_fields' in kwargs
        ):
            kwargs['update_fields'] = (
                tuple(kwargs['update_fields']) + ('modified', ))

    @classmethod
    def get_object_relations(cls, obj_id):
        """
        Функция для определения моделей и идентификаторов,
        объектов зависимых от экземпляра данного класса.
        Экземпляр класса задается через cls и obj_id

        :param cls: Класс экземпляра, от которого будем искать зависимых
        :param obj_id: ID экземпляра от которого будем искать зависимых
        :return: Кортеж кортежей вида:
            (
                (ModelClass_1, ValuesListQuerySet(id1, id2, ...) ),
                (ModelClass_2, ValuesListQuerySet(id1, id2, id3 ...) )
                ...
                (ModelClass_N, ValuesListQuerySet(id1, ...))
            )
        """
        # Находим все соотношения с другими объектами:
        _relations = get_all_related_objects(cls)
        result = []
        for rel in _relations:
            # Имя поля, которое ссылается на наш объект в зависимой модели:
            _attname = rel.field.attname
            if _attname.endswith('_id'):
                _attname = _attname.replace('_id', '')
            _attname = '%s__pk' % _attname
            # Пытаемся определить наличие зависимых объектов:
            pks = rel.field.model.objects.filter(
                **{str(_attname): obj_id}
            ).values_list('pk')
            if pks.exists():
                result.append((rel.field.model, pks))

        return tuple(result)

    @classmethod
    def get_verbose_object_relations(cls, obj_id):
        """
        Функция для определения наименований моделей,
        объектов зависимых от экземпляра данного класса.
        Экземпляр класса задается через cls и obj_id

        :param cls: Класс экземпляра, от которого будем искать зависимых
        :param obj_id: ID экземпляра от которого будем искать зависимых
        :return: Кортеж вида:
            (
                u"ModelClassName_1",
                u"ModelClassName_2",
                ...
                u"ModelClassName_N",
            )
        """
        relations = cls.get_object_relations(obj_id)
        # pylint: disable=consider-using-generator
        return tuple([rel[0]._meta.verbose_name for rel in relations])

    def get_prohibit_delete_info(self):
        """
        Возвращает словарь зависимых объектов,
        запрещающих удаление, при наличии
        указанного у модели списка PROHIBIT_DELETE_RELATIONS
        {class.__name__: set([obj1, obj2]), }
        Либо пустой словарь, если таких зависимых объектов не найдено
        """
        self_c_name = self.__class__.__name__
        relations_names = self.PROHIBIT_DELETE_RELATIONS
        # pylint: disable=consider-using-dict-comprehension
        return dict([
            (c, objs) for (c, objs) in self.get_related_objects() if (
                # исключение себя и проверка наличия в списке исключений
                c.__name__ is not self_c_name and c.__name__ in relations_names
            )
        ])

    @staticmethod
    def validate_field_choices(obj, field_list=None):
        """
        Функция проверяет соответствие значений полей объекта модели указанным
        choices. В случае не соответствия генерируется исключение ValueError.
        Может принимать в параметрах список с полями, которые необходимо
        проверить, если таковой не указан, то фунцкия проверяет все поля.
        :param obj:
        :param field_list:
        """
        fields = [f for f in obj.__class__._meta.fields if bool(f.choices)]
        if field_list:
            fields = [f for f in fields if f.name in field_list]
        for field in fields:
            choices = [key_value[0] for key_value in field.choices]
            if not getattr(obj, field.name) in choices:
                # pylint: disable=consider-using-f-string
                raise ValueError(
                    "Value `%s` of the field `%s` doesn't match to possible"
                    " choices. The choices are: (%s)"
                    % (getattr(obj, field.name), field.name, ', '.join(
                        map(str, choices))))

    def clean(self):
        errors = defaultdict(list)
        try:
            super().clean()
        except ValidationError as error:
            errors.update(error.update_error_dict(errors))

        self.simple_clean(errors)

        if errors:
            raise ValidationError(errors)

    def simple_clean(self, errors):
        """
        Упрощенная проверка на ошибки.

        :param defaultdict(list) errors: словарь ошибок
        """

    class Meta:
        abstract = True


class SimpleDictionary(BaseModel):
    """
    Класс простого справочника, содержащего только Код и Наименование
    """
    MUST_BE_UNIQUE = True

    # Уникальность code и name среди школы и ее родителей
    MUST_BE_UNIQUE_WITH_PARENTS_SCHOOL = False

    # Уникальность code и name в периоде
    MUST_BE_UNIQUE_WITH_PERIOD = False

    code = models.CharField(
        'Код',
        max_length=20,
        db_index=True
    )
    name = models.CharField(
        'Наименование',
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return self.name or ''

    def display(self):
        return self.name or ''
    display.json_encode = True

    def save(self, *args, **kwargs):
        if self.MUST_BE_UNIQUE:
            self.code = (self.code or '').strip()
            self.name = (self.name or '').strip()

            if not self.code:
                self.code = get_unique_code(self.__class__)

            if not self.name:
                raise ValidationError(
                    'Наименование не может быть пустым!')

            current_objs = self.__class__.objects.exclude(id=self.id)
            if hasattr(self, 'school'):
                if self.MUST_BE_UNIQUE_WITH_PARENTS_SCHOOL:
                    current_objs = current_objs.filter(
                        school__lft__lte=self.school.lft,
                        school__rght__gte=self.school.rght,
                        school__tree_id=self.school.tree_id,
                    )
                else:
                    current_objs = current_objs.filter(school=self.school)

            if hasattr(self, 'period') and self.MUST_BE_UNIQUE_WITH_PERIOD:
                current_objs = current_objs.filter(period=self.period)

            if current_objs.filter(code__iexact=self.code).exists():
                raise ValidationError(
                    'Объект с данным кодом уже существует!')

            if current_objs.filter(name__iexact=self.name).exists():
                raise ValidationError(
                    'Объект с данным наименованием уже существует!')

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
