from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.lib_example_types.domain import (
    ExampleTypeNotFound,
    factory,
)


class ExampleTypeValidator(Validator):
    """Валидатор типа библиотечных экземпляров."""

    def validate_existence(self) -> 'ExampleTypeValidator':
        try:
            self._uow.example_types.get_object_by_id(self._data.id)
        except ExampleTypeNotFound as exc:
            self._errors['id'].append(str(exc))
            self._skip_chain = True

        return self

    @may_skip
    def validate_name(self) -> 'ExampleTypeValidator':
        if 'name' in self._data.dict():
            name = self._data.name.strip()
            if name:
                example_type = factory.create(self._data)
                if self._uow.example_types.is_exists(example_type):
                    self._errors['name'].append('Такой тип библиотечных экземпляров уже существует')

        return self
