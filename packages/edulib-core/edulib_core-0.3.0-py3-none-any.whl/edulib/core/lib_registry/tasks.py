# pylint: disable=expression-not-assigned, broad-exception-caught, too-many-statements
from django.db.transaction import (
    atomic,
)
from django.utils.encoding import (
    force_str,
)

from .helpers import (
    calc_writeoff_reasons,
    delete_lib_summary_book_without_examples,
)
from .models import (
    LibSummaryBook,
    LibSummaryBookCalculated,
    LibSummaryBookCatalog,
    LibSummaryBookDisposal,
    LibSummaryBookDisposalCatalog,
    LibSummaryBookDisposalTypes,
    LibSummaryBookTypes,
)


def _run_calc_summary_book(connection=None):  # noqa: C901
    """Подсчет документов в КСУ."""
    def _calc_types(lsb, model_type):
        """Подсчет документов по типам.

        :param lsb LibSummaryBook() or LibSummaryBookDisposal(): экземпляр КСУ
        :param model_type Model: модель количества документов по типам
        """
        for (
            lib_example_type_id,
            books_count
        ) in list(lsb.get_examples_types_count.items()):
            lsb_type = model_type.objects.filter(
                lib_summary_book_id=lsb.id,
                lib_example_type_id=lib_example_type_id,
            ).first()
            if not lsb_type:
                lsb_type = model_type()
                lsb_type.lib_summary_book_id = lsb.id
                lsb_type.lib_example_type_id = lib_example_type_id
            lsb_type.books_count = books_count
            lsb_type.save()

    def _calc_bbc(lsb, model_bbc):
        """Подсчет документов по разделам ББК.

        :param lsb LibSummaryBook() or LibSummaryBookDisposal(): экземпляр КСУ
        :param model_bbc Model: модель количества документов по разделам ББК
        """
        lsb_bbc_on_create = []
        lsb_bbc_on_update = []
        for bbc_id, books_count in list(lsb.get_examples_bbc_count.items()):
            on_create = False
            lsb_bbc = model_bbc.objects.filter(
                lib_summary_book_id=lsb.id,
                bbc_id=bbc_id,
            ).first()
            if not lsb_bbc:
                lsb_bbc = model_bbc()
                lsb_bbc.lib_summary_book_id = lsb.id
                lsb_bbc.bbc_id = bbc_id
                on_create = True

            if on_create or lsb_bbc.books_count != books_count:
                lsb_bbc.books_count = books_count
                lsb_bbc_on_create.append(lsb_bbc) if on_create else lsb_bbc_on_update.append(lsb_bbc)
        if lsb_bbc_on_create:
            model_bbc.objects.bulk_create(lsb_bbc_on_create)
        if lsb_bbc_on_update:
            model_bbc.objects.bulk_update(lsb_bbc_on_update, fields=['books_count'])

    def _calc_lsb(lsb):
        """Подсчет итогов в КСУ.

        :param lsb LibSummaryBook() or LibSummaryBookDisposal(): экземпляр КСУ
        """
        for attr in [
            'examples_count',
            'names_count',
            'examples_sum',
            'examples_on_balance_count',
            'names_on_balance_count',
            'examples_on_balance_sum',
            'examples_no_balance_count',
            'names_no_balance_count',
            'examples_no_balance_sum',
        ]:
            setattr(lsb, attr, getattr(lsb, f'get_{attr}', 0))
        lsb.save()

    def calc_lib_summary_book(school):
        """Подсчитывает итоги в КСУ для поступлений."""
        # Удаление записей без экземпляров в ОО.
        delete_lib_summary_book_without_examples(school.id, connection=connection)
        for lib_summary_book in LibSummaryBook.objects.filter(school=school):
            # Заполним количества и суммы для записи КСУ:
            _calc_lsb(lib_summary_book)
            # Присвоим номер записи КСУ:
            lib_summary_book.inflow_record_number = (
                lib_summary_book.get_inflow_record_number
            )
            lib_summary_book.save()
            # Посчитаем документы по типам и разделам ББК:
            _calc_types(lib_summary_book, LibSummaryBookTypes)
            _calc_bbc(lib_summary_book, LibSummaryBookCatalog)

    def calc_disposal_lib_summary_book(school):
        """Подсчитывает итоги в КСУ для выбытий."""
        empty_ids = []  # Записи в КСУ, по которым нет экземпляров или дубли
        for lib_summary_disp in LibSummaryBookDisposal.objects.filter(
            school=school
        ):
            if not lib_summary_disp.get_examples_count:
                # по записи нет экземпляров. Добавим в список для удаления:
                empty_ids.append(lib_summary_disp.id)
            elif lib_summary_disp.id not in empty_ids:
                # Заполним количества и суммы для записи КСУ:
                _calc_lsb(lib_summary_disp)
                # Заполним источники поступлений:
                lib_summary_disp.disposal_source = (
                    lib_summary_disp.get_disposal_source
                )
                lib_summary_disp.save()
                # Посчитаем экз-ры по типам, разделам ББК и причинам списания:
                _calc_types(lib_summary_disp, LibSummaryBookDisposalTypes)
                _calc_bbc(lib_summary_disp, LibSummaryBookDisposalCatalog)
                calc_writeoff_reasons(lib_summary_disp)

                # Найдём дубли:
                doubles_ids = LibSummaryBookDisposal.objects.filter(
                    school_id=lib_summary_disp.school_id,
                    record_date=lib_summary_disp.record_date,
                    writeoff_act_number=lib_summary_disp.writeoff_act_number
                ).exclude(
                    id=lib_summary_disp.id
                ).values_list('id', flat=True)
                # Добавим дубли в список для удаления:
                empty_ids.extend(doubles_ids)

        if empty_ids:
            LibSummaryBookDisposal.objects.filter(id__in=empty_ids).delete()

    # Расчёт КСУ только среди библиотек школ, где были изменения.
    for school_lsb in LibSummaryBookCalculated.objects.filter(
        calculated=False
    ):
        try:
            with atomic():
                calc_lib_summary_book(school_lsb.school)
            with atomic():
                calc_disposal_lib_summary_book(school_lsb.school)
        except Exception as exc:
            # На всякий случай ограничим длину сохраняемого сообщения,
            # что бы точно помещалось в длину поля
            school_lsb.note = force_str(exc)[:255]
        else:
            school_lsb.calculated = True
            school_lsb.note = 'Выполнено'
        school_lsb.save()
