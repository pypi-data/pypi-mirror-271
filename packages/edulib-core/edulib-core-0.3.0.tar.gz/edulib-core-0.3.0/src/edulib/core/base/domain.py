class BaseEnumerate:
    """
    Базовый класс для создания перечислений.
    """
    # В словаре values описываются перечисляемые константы
    # и их человеческое название
    # Например: {STATE1: u'Состояние 1', CLOSED: u'Закрыто'}
    values = {}

    @classmethod
    def get_choices(cls):
        """
        Используется для ограничения полей ORM и в качестве источника данных
        в ArrayStore и DataStore ExtJS
        """
        return list(cls.values.items())

    get_items = get_choices

    @classmethod
    def get_constant_value_by_name(cls, name):
        """
        Возвращает значение атрибута константы, которая используется в
        качестве ключа к словарю values
        """
        if not isinstance(name, str):
            raise TypeError("'name' must be a string")

        if not name:
            raise ValueError("'name' must not be empty")

        return cls.__dict__[name]
