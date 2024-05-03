from typing import (
    TYPE_CHECKING,
)

from explicit.domain import (
    asdict,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
    handle_pydantic_validation_error,
)

from edulib.core.lib_example_types import (
    domain,
)
from edulib.core.lib_example_types.services.validators import (
    ExampleTypeValidator,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


@handle_pydantic_validation_error
def create_example_type(
    command: domain.CreateExampleType,
    uow: 'UnitOfWork',
) -> domain.ExampleType:
    with uow.wrap():
        example_type = domain.ExampleTypeDTO(**asdict(command))

        validator = ExampleTypeValidator(example_type, uow)
        errors = validator.validate_name().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.create_example_type(example_type, uow)


@handle_pydantic_validation_error
def update_example_type(
    command: domain.UpdateExampleType,
    uow: 'UnitOfWork',
) -> domain.ExampleType:
    with uow.wrap():
        example_type = domain.ExampleTypeDTO(**asdict(command))

        validator = ExampleTypeValidator(example_type, uow)
        errors = validator.validate_existence().validate_name().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.update_example_type(example_type, uow)


@handle_pydantic_validation_error
def delete_example_type(
    command: domain.DeleteExampleType,
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        example_type = domain.ExampleTypeDTO(**asdict(command))

        validator = ExampleTypeValidator(example_type, uow)
        errors = validator.validate_existence().get_errors()
        if errors:
            raise DomainValidationError(errors)

        domain.delete_example_type(example_type, uow)
