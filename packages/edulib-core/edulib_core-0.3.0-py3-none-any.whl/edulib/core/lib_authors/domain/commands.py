from explicit.messagebus.commands import (
    Command,
)


class CreateAuthor(Command):

    name: str

    class Config:
        title = 'Команда создания автора'


class UpdateAuthor(Command):

    id: int
    name: str

    class Config:
        title = 'Команда обновления автора'


class DeleteAuthor(Command):

    id: int

    class Config:
        title = 'Команда удаления автора'
