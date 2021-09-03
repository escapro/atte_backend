from django.db.models.query import QuerySet
from crm.utils.working_day import get_active_working_day
from django.contrib.auth.models import User
from main.models import Employee
from crm.models import Cashbox, Expense, Shift, ShiftType, WorkingDay
from typing import Optional
from django.db.models import Sum
from crm.utils.common import debug


def get_employee_active_shift(user: User) -> Optional[Shift]:
    """
    Возвращает активную смену сотрудника
    
    :param User user: Сотрудник на которого нужно ссылаться
    """

    shift = None

    active_wd = get_active_working_day(create=False)

    if active_wd:
        active_shift = Shift.objects.filter(working_day=active_wd, employee=Employee.objects.get(user=user), finished=False).last()
        if active_shift:
            shift = active_shift

    return shift


def get_active_shifts() -> Optional[QuerySet[Shift]]:
    """
    Возвращает все активные смены
    """

    shifts = None

    active_wd = get_active_working_day(create=False)

    if active_wd:
        active_shifts = Shift.objects.filter(working_day=active_wd, finished=False)
        if active_shifts:
            shifts = active_shifts

    return shifts


def calculate_shift_fact(shift, data):
    """
    Просчитывает отчетность конца смены
    """

    result = {}

    result['cash_income'] = 0
    result['noncash_income'] = 0
    result['shift_income'] = 0
    result['cash_difference'] = 0
    result['noncash_difference'] = 0
    result['fact'] = False

    # cash_income
    result['cash_income'] = data['cash_end'] - data['cash_start']

    expenses_sum = Expense.objects.filter(working_day=shift.working_day, cashbox=shift.cashbox, shift_type=shift.shift_type).aggregate(Sum('sum'))
    if expenses_sum['sum__sum']:
        result['cash_income'] += expenses_sum['sum__sum']

    # noncash_income
    result['noncash_income'] = data['noncash_end'] - data['noncash_start']

    # shift_income
    result['shift_income'] = result['cash_income'] + result['noncash_income']

    # fact
    sales_fact = data['sales']
    cashboxFact_fact = data['cashbox_fact']
    cash_refund_fact = data['cash_refund']
    noncash_refund_fact = data['noncash_refund']

    last_shift = Shift.objects.exclude(pk=shift.pk).filter(working_day=shift.working_day, cashbox=shift.cashbox).last()

    if last_shift:
        sales_fact -= last_shift.sales
        cashboxFact_fact -= last_shift.cashbox_fact
        cash_refund_fact -= last_shift.cash_refund
        noncash_refund_fact -= last_shift.noncash_refund

    if (result['noncash_income'] == (sales_fact - cashboxFact_fact - noncash_refund_fact )) and (result['cash_income'] == (cashboxFact_fact - cash_refund_fact)):
            result['fact'] = True

    # cash_difference
    result['cash_difference'] = result['cash_income'] - (cashboxFact_fact - noncash_refund_fact)

    # noncash_difference
    result['noncash_difference'] = result['noncash_income'] - (sales_fact - cashboxFact_fact - noncash_refund_fact)

    return result