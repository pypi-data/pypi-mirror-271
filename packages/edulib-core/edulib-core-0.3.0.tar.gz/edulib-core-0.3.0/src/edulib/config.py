from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


@dataclass
class Config:
    max_upload_size: int = Field(
        title='Максимальный размер загружаемого файла',
        default=5242880
    )
    calc_lib_summary_book_min: int = Field(
        title='Интервал запуска задачи подсчета документов в КСУ в минутах',
        default=60
    )
    use_default_bbc_sections: bool = Field(
        title='Использовать разделы ББК по-умолчанию',
        default=False
    )
    uploads_dir: str = Field(
        title='Каталог для загрузки файлов',
        default='uploads'
    )
