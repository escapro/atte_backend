import calendar

from crm.models import ShiftPayrollPeriod
from crm.utils.common import debug


def get_payroll_periods(date):
    """
    Возвращяет объект PayrollPeriod в форматтированном виде
    """

    periods = ShiftPayrollPeriod.objects.filter(is_active=True)
    formatted_periods = {}

    for period in periods:
        formatted_periods[period.day] = format_payroll_period(period.day, date.month, date.year)

    return formatted_periods


def format_payroll_period(value, month, year):
    if not value.isnumeric():
        if value == 'end':
            return int(calendar.monthrange(year, month)[1])

    return int(value)


def get_payroll_period(date):
    formatted_payroll_periods = get_payroll_periods(date)
    day = date.day
    period_value = None

    for key, value in formatted_payroll_periods.items():
        if int(day) <= int(value):
            period_value = key
            break

    return ShiftPayrollPeriod.objects.filter(day=period_value)[0]