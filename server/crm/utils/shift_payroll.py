import decimal

from crm.models import Shift
from crm.models import ShiftPayrollPeriod, ShiftPayroll, ShiftType
from crm.utils.bonuses import get_bonus_rate
from crm.utils.common import debug
from crm.utils.shift_payroll_period import format_payroll_period, get_payroll_periods, get_payroll_period
from main.models import Employee


def update_shift_payroll_data(shift: Shift, work_time):
    """
    Обновляет значение заработка на смене и процетов, а также создает новую запись в случае его отсутствия
    """

    payroll_period = get_payroll_period(shift.working_day.date)
    bonus_rate = get_bonus_rate(shift.shift_type, shift.shift_income)

    per_minute_rate = shift.shift_type.hourly_rate / 60
    per_second_rate = per_minute_rate / 60

    payroll = ShiftPayroll.objects.create(shift=shift, period=payroll_period)

    payroll.from_shift = payroll.from_shift + (decimal.Decimal(work_time * per_second_rate))
    payroll.from_interest = payroll.from_interest + (decimal.Decimal(shift.shift_income * bonus_rate / 100))

    payroll.save()
