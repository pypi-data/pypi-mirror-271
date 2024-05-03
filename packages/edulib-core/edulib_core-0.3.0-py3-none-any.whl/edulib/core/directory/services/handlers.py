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

from edulib.core.directory import (
    domain,
)
from edulib.core.directory.services.validators import (
    BbkValidator,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


@handle_pydantic_validation_error
def create_bbk(
    command: domain.CreateBbk,
    uow: 'UnitOfWork',
) -> domain.Bbk:
    with uow.wrap():
        bbk = domain.BbkDTO(**asdict(command))

        validator = BbkValidator(bbk, uow)
        errors = validator.validate_parent().validate_code().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.create_bbk(bbk, uow)


@handle_pydantic_validation_error
def update_bbk(
    command: domain.UpdateBbk,
    uow: 'UnitOfWork',
) -> domain.Bbk:
    with uow.wrap():
        bbk = domain.BbkDTO(**asdict(command))

        validator = BbkValidator(bbk, uow)
        errors = validator.validate_existence().validate_parent().validate_code(is_update=True).get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.update_bbk(bbk, uow)


@handle_pydantic_validation_error
def delete_bbk(
    command: domain.DeleteBbk,
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        bbk = domain.BbkDTO(**asdict(command))

        validator = BbkValidator(bbk, uow)
        errors = validator.validate_existence().get_errors()
        if errors:
            raise DomainValidationError(errors)

        domain.delete_bbk(bbk, uow)
