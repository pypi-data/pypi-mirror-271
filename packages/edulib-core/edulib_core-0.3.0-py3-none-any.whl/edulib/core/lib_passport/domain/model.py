WEEK_ENUM = [{
    'name': 'shedule_mon',
    'label': 'Понедельник',
    'day_num': 0
}, {
    'name': 'shedule_tue',
    'label': 'Вторник',
    'day_num': 1
}, {
    'name': 'shedule_wed',
    'label': 'Среда',
    'day_num': 2
}, {
    'name': 'shedule_thu',
    'label': 'Четверг',
    'day_num': 3
}, {
    'name': 'shedule_fri',
    'label': 'Пятница',
    'day_num': 4
}, {
    'name': 'shedule_sat',
    'label': 'Суббота',
    'day_num': 5
}, {
    'name': 'shedule_sun',
    'label': 'Воскресенье',
    'day_num': 6
}]


class PassportNotFound(Exception):
    """Возбуждается, когда паспорт библиотеки не может быть определен."""

    def __init__(self, *args):
        super().__init__('Паспорт библиотеки не найден', *args)
