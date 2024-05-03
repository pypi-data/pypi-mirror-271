from typing import (
    Optional,
)

from explicit.domain import (
    asdict,
)

from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.directory.domain import (
    Bbk,
    BbkDTO,
    BbkNotFound,
    factory,
)


class BbkValidator(Validator):
    """Валидатор раздела ББК."""

    def validate_existence(self) -> 'BbkValidator':
        if not self._get_bbk(self._data.id, 'id'):
            self._skip_chain = True

        return self

    @may_skip
    def validate_parent(self) -> 'BbkValidator':
        if self._data.parent_id:
            self._get_bbk(self._data.parent_id, 'parent_id')

        return self

    @may_skip
    def validate_code(self, *, is_update: bool = False) -> 'BbkValidator':
        if 'code' in self._data.dict():
            code = self._data.code.strip()
            if code:
                if is_update:
                    bbk = self._get_bbk(self._data.id, 'id')
                    dto = BbkDTO(**asdict(bbk) | self._data.dict())
                else:
                    dto = self._data

                if self._uow.bbk.is_exists(factory.create(dto)):
                    self._errors['code'].append('Такой раздел ББК уже существует')

        return self

    def _get_bbk(self, identifier: int, error_name: str) -> Optional[Bbk]:
        try:
            return self._uow.bbk.get_object_by_id(identifier)
        except BbkNotFound as exc:
            self._errors[error_name].append(str(exc))
