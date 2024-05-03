from typing import (
    TYPE_CHECKING,
)

from edulib.core.lib_example_types.domain.factories import (
    ExampleTypeDTO,
    factory,
)
from edulib.core.utils.tools import (
    modify,
)


if TYPE_CHECKING:
    from edulib.core.lib_example_types.domain.model import (
        ExampleType,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )



def create_example_type(data: ExampleTypeDTO, uow: 'UnitOfWork') -> 'ExampleType':
    """Сервис создания типа библиотечных экземпляров."""
    example_type = factory.create(data)
    uow.example_types.add(example_type)
    assert example_type.id is not None, example_type

    return example_type


def update_example_type(data: ExampleTypeDTO, uow: 'UnitOfWork') -> 'ExampleType':
    """Сервис обновления типа библиотечных экземпляров."""
    example_type = uow.example_types.get_object_by_id(data.id)
    modify(example_type, **data.dict(exclude={'id'}))
    uow.example_types.update(example_type)

    return example_type


def delete_example_type(data: ExampleTypeDTO, uow: 'UnitOfWork') -> None:
    """Сервис удаления типа библиотечных экземпляров."""
    example_type = uow.example_types.get_object_by_id(data.id)
    uow.example_types.delete(example_type)
