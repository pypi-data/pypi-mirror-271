from edulib.core.base.domain import (
    BaseEnumerate,
)


class MonthEnum(BaseEnumerate):
    """Перечисление месяцев."""

    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12

    values = {
        JAN: 'Январь',
        FEB: 'Февраль',
        MAR: 'Март',
        APR: 'Апрель',
        MAY: 'Май',
        JUN: 'Июнь',
        JUL: 'Июль',
        AUG: 'Август',
        SEP: 'Сентябрь',
        OCT: 'Октябрь',
        NOV: 'Ноябрь',
        DEC: 'Декабрь',
    }


class ReadingRoomTypeEnum(BaseEnumerate):
    """Тип читального зала."""

    COMBINED, INDIVIDUAL = 1, 2
    values = {
        COMBINED: 'совмещен с абонементом',
        INDIVIDUAL: 'отдельный',
    }
