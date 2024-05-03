from dataclasses import (
    asdict,
)
from typing import (
    Generator,
)

from django.core.exceptions import (
    ObjectDoesNotExist,
)
from explicit.adapters.db import (
    AbstractRepository,
)

from edulib.core.lib_authors import (
    models as db,
)
from edulib.core.lib_authors.domain.model import (
    Author,
    AuthorNotFound,
)


class AuthorRepository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> Author:
        """Получает объект по идентификатору."""
        try:
            db_instance = db.LibraryAuthors.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as e:
            raise AuthorNotFound() from e

    def add(self, obj: Author) -> Author:
        assert isinstance(obj, Author)

        return self._to_db(obj)

    def update(self, obj: Author) -> Author:
        assert isinstance(obj, Author)

        return self._to_db(obj)

    def delete(self, obj: Author) -> None:
        assert isinstance(obj, Author)
        db.LibraryAuthors.objects.get(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[Author, None, None]:
        for author in db.LibraryAuthors.objects.iterator():
            yield self._to_domain(author)

    def author_exists(self, author: Author) -> bool:
        """Предикат: существует ли автор с указанным именем."""
        return db.LibraryAuthors.objects.exclude(pk=author.id).filter(name__iexact=author.name).exists()

    def _to_db(self, modelinstance: Author) -> Author:
        assert isinstance(modelinstance, Author)

        db_instance, _ = db.LibraryAuthors.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )
        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.LibraryAuthors) -> Author:
        return Author(
            id=dbinstance.pk,
            name=dbinstance.name,
        )


repository = AuthorRepository()
