from crm.utils.datetime import format_with_zero
from crm.utils.common import debug
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
        debug("error", '1')
        return None

    shifts = Shift.objects.filter(working_day=wd)

    if not shifts:
        debug("error", '2')
        return None

    cash_income = shifts.aggregate(Sum('cash_income'))
    noncash_income = shifts.aggregate(Sum('noncash_income'))

    if cash_income['cash_income__sum'] is None or noncash_income['noncash_income__sum'] is None:
        debug("cash_income['cash_income__sum']", cash_income['cash_income__sum'])
        debug("noncash_income['noncash_income__sum']", noncash_income['noncash_income__sum'])
        debug("error", '3')
        return None

    return {
        "cash_income": cash_income['cash_income__sum'],
        "noncash_income": noncash_income['noncash_income__sum'],
        "total_income": cash_income['cash_income__sum'] + noncash_income['noncash_income__sum']
    }


def get_wds_pagination_data(active_month):
    result = {'months': []}

    MonthL = ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль', 'Август','Сентябрь','Октябрь','Ноябрь', 'Декабрь']

    working_days = WorkingDay.objects.all()

    for wd in working_days.values('date__day', 'date__month', 'date__year').distinct('date__month'):
        month_name = MonthL[wd['date__month']-1]

        url_params = {
            "from_date": "{}-{}-{}".format(wd['date__year'], format_with_zero(wd['date__month']), '01'),
            "to_date": "{}-{}-{}".format(wd['date__year'], format_with_zero(wd['date__month']+1 if wd['date__month']<12 else 1), '01')
        }

        if not month_name in result['months']:
            result['months'].append({
                "name": month_name,
                "is_active": True if active_month.month==wd['date__month'] else False,
                "number": wd['date__month'],
                "url_params": url_params
            })

    return result