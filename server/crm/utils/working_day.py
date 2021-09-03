from typing import Optional, Tuple

from django.db.models.aggregates import Sum
from crm.models import Shift, WorkingDay
import datetime

def get_last_working_day() -> Optional[WorkingDay]:
    """
    Возвращает последнюю смену
    """

    return WorkingDay.objects.all().order_by('date').last()

def get_active_working_day(create: bool = False) -> Optional[WorkingDay]:
    """
    Возвращает последнюю активную смену

    :param bool create: Создавать новую смену, при отсутствии
    """

    working_day = None

    last_working_day = get_last_working_day()
    today = datetime.date.today()

    if not last_working_day:
        if create:
            working_day = WorkingDay.objects.create(date=today)
    else:
        if last_working_day.finished:
            if create and today != last_working_day.date:
                working_day = WorkingDay.objects.create(date=today)
        else:
            working_day = last_working_day

    return working_day


def calculate_wd_income(working_day: WorkingDay = None) -> Optional[dict]:
    """
    Подсчитывает выручку рабочего дня
    """

    wd = working_day if working_day else get_active_working_day()
    if not wd:
        return None

    shifts = Shift.objects.filter(working_day=wd)

    if not shifts:
        return None

    cash_income = shifts.aggregate(Sum('cash_income'))
    noncash_income = shifts.aggregate(Sum('noncash_income'))

    if not cash_income['cash_income__sum'] or not noncash_income['noncash_income__sum']:
        return None

    return {
        "cash_income": cash_income['cash_income__sum'],
        "noncash_income": noncash_income['noncash_income__sum'],
        "total_income": cash_income['cash_income__sum'] + noncash_income['noncash_income__sum']
    }