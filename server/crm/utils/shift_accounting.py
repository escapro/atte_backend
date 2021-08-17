
from crm.models import Expense, Shift, ShiftType, WorkingDay
from django.db.models import Sum

def process_shift_data(data):
    new_data = data

    new_data['cash_income'] = 0
    new_data['noncash_income'] = 0
    new_data['shift_income'] = 0
    new_data['fact'] = False
    new_data['cash_difference'] = 0
    new_data['noncash_difference'] = 0

    wd = WorkingDay.objects.get(id=data['working_day'])
    st = ShiftType.objects.get(id=data['shift_type'])

    # cash_income
    new_data['cash_income'] = data['cash_end'] - data['cash_start']

    expenses_sum = Expense.objects.filter(working_day=wd, shift_type=st).aggregate(Sum('sum'))

    if expenses_sum['sum__sum']:
        new_data['cash_income'] += expenses_sum['sum__sum']


    # noncash_income
    new_data['noncash_income'] = data['noncash_end'] - data['noncash_start']


    # shift_income
    new_data['shift_income'] = new_data['cash_income'] + new_data['noncash_income']


    # fact
    sales_fact = data['sales']
    cashboxFact_fact = data['cashbox_fact']
    cash_refund_fact = data['cash_refund']
    noncash_refund_fact = data['noncash_refund']

    shifts = Shift.objects.filter(working_day=wd)

    if len(shifts) >= 1:
        last_shift = shifts.last()
        sales_fact -= last_shift.sales
        cashboxFact_fact -= last_shift.cashbox_fact
        cash_refund_fact -= last_shift.cash_refund
        noncash_refund_fact -= last_shift.noncash_refund

    if (new_data['noncash_income'] == (sales_fact - cashboxFact_fact - noncash_refund_fact )) and \
        (new_data['cash_income'] == (cashboxFact_fact - cash_refund_fact)):
            new_data['fact'] = True


    # cash_difference
    new_data['cash_difference'] = new_data['cash_income'] - (cashboxFact_fact - noncash_refund_fact)

    # noncash_difference
    new_data['noncash_difference'] = new_data['noncash_income'] - (sales_fact - cashboxFact_fact - noncash_refund_fact)

    return new_data