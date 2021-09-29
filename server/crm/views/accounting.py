from crm.utils.datetime import get_today_datetime
import rest_framework
from crm.utils.working_day import get_wds_pagination_data
from crm.utils.accounting import calculate_by_formula
from django.db import models
from crm.utils.common import debug
from crm.models import AdditionalExpense, Cashbox, Expense, ExpenseCategory, Shift, ShiftType, WorkingDay
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdminManager, isClientUser
from rest_framework import status
from datetime import datetime, timedelta
from django.db.models import Sum
import calendar


def generate_shift_data(s, shift_types):
    result = {}

    for st in shift_types:
        shift = s.filter(shift_type=st)

        cash_income_sum = 0
        noncash_income_sum = 0
        total_income_sum = 0
        cash_difference_sum = 0
        noncash_difference_sum = 0
        cash_refund_sum = 0
        noncash_refund_sum = 0

        cash_income = shift.values('cash_income').aggregate(
            sum=Sum('cash_income'))['sum']
        noncash_income = shift.values('noncash_income').aggregate(
            sum=Sum('noncash_income'))['sum']
        total_income = shift.values('shift_type').aggregate(
            sum=Sum('shift_income'))['sum']
        cash_difference = shift.values('cash_difference').aggregate(
            sum=Sum('cash_difference'))['sum']
        noncash_difference = shift.values('noncash_difference').aggregate(
            sum=Sum('noncash_difference'))['sum']
        cash_refund = shift.values('cash_refund').aggregate(
            sum=Sum('cash_refund'))['sum']
        noncash_refund = shift.values('noncash_refund').aggregate(
            sum=Sum('noncash_refund'))['sum']

        if cash_income:
            cash_income_sum = cash_income
        if noncash_income:
            noncash_income_sum = noncash_income
        if total_income:
            total_income_sum = total_income
        if cash_difference:
            cash_difference_sum = cash_difference
        if noncash_difference:
            noncash_difference_sum = noncash_difference
        if cash_refund:
            cash_refund_sum = cash_refund
        if noncash_refund:
            noncash_refund_sum = noncash_refund

        result[st.id] = {}
        result[st.id]['id'] = st.id
        result[st.id]['shift_type_name'] = st.name
        result[st.id]['cash_income'] = cash_income_sum
        result[st.id]['noncash_income'] = noncash_income_sum
        result[st.id]['total_income'] = total_income_sum
        result[st.id]['cash_difference'] = cash_difference_sum
        result[st.id]['noncash_difference'] = noncash_difference_sum
        result[st.id]['cash_refund'] = cash_refund_sum
        result[st.id]['noncash_refund'] = noncash_refund_sum

    return result


def generate_expenses_data(expenses, expenses_category):
    result = []

    for ec in expenses_category:
        expense = expenses.filter(expense_category=ec)

        total_sum = 0

        total = expense.values('sum').aggregate(sum=Sum('sum'))['sum']

        if total:
            total_sum = total

        result.append({
            "category": ec.name,
            "sum": total_sum
        })

    return result


def get_total_expenses_data(wds):
    result = {}

    for ec in ExpenseCategory.objects.filter(is_accounting_expense=True):
        result[ec.name] = 0

    for wd in wds:
        expenses = Expense.objects.filter(working_day=wd, expense_category__is_accounting_expense=True)
        for exp in expenses:
            result[exp.expense_category.name] += exp.sum

    return result


def get_additional_expenses_data(params, variables):
    result = {
        "total": 0,
        "data": []
    }

    date__range = [params['from_date'], params['to_date']]

    additional_expenses = AdditionalExpense.objects.filter(date__range=date__range)

    for expense in additional_expenses:
        expense_name = expense.name

        if not expense.name:
            expense_name = expense.additional_expense_category.name

        if expense.sum == None and expense.calculation_formula == None:
            return None

        result['data'].append({
            "id": expense.id,
            "name": expense_name,
            "date": expense.date,
            "sum": expense.sum if expense.sum else calculate_by_formula(expense.calculation_formula, variables),
            "formula": expense.calculation_formula,
        })

    for expense in result["data"]:
        if not expense['sum'] == None:
            result['total'] += expense['sum']




    # for wd in wds:
    #     add_expenses = AdditionalExpense.objects.filter(date=wd.date)
    #     for add_expense in add_expenses:
    #         expense_name = ''

    #         if not add_expense.name:
    #             expense_name = add_expense.additional_expense_category.name
    #         else:
    #             expense_name = add_expense.name

    #         if not expense_name in result["data"]:
    #             result["data"][expense_name] = {}
    #             result["data"][expense_name]['value'] = 0

    #         if not add_expense.sum and not add_expense.calculation_formula:
    #             return None

    #         if not add_expense.sum:
    #             sum = calculate_by_formula(add_expense.calculation_formula, variables)

    #             result["data"][expense_name]['formula'] = add_expense.calculation_formula

    #             if sum == None:
    #                 result["data"][expense_name]['value'] = None
    #             else:
    #                 result["data"][expense_name]['value'] += sum
    #         else:
    #             result["data"][expense_name]['formula'] = ''
    #             result["data"][expense_name]['value'] += add_expense.sum

    #         result["data"][expense_name]['date'] = add_expense.date

    # for key in result["data"]:
    #     if not result["data"][key]['value'] == None:
    #         result['total'] += result["data"][key]['value']

    return result

def apply_filters_by_params(object, params):
    wds = object

    date__range = [params['from_date'], params['to_date']]

    wds = wds.filter(date__range=date__range)

    return wds

def add_non_work_days_data(data, params):
    result = data

    month = params.get('date__month', None)
    year = params.get('date__year', None)

    days_range = calendar.monthrange(int(year), int(month))[1]

    for day in range(days_range):
        day+=1
        is_day_exist = False
        for d in data:
            if day == d['date']['day']:
                is_day_exist = True

        if not is_day_exist:
            new_data = {}

            date = datetime(int(year), int(month), int(day))

            DayL = ['Пн','Вт','Ср','Чт','Пт','Сб','Вс']

            new_data['is_work_day'] = False
            new_data['date'] = {}
            new_data['date']['week'] = DayL[date.weekday()]
            new_data['date']['day'] = date.day
            new_data['date']['month'] = date.month
            new_data['date']['year'] = date.year
        else:
            continue

        result.append(new_data)

    result = sorted(result, key=lambda k: k['date']['day'])

    return result


class AccountingView(APIView):
    permission_classes = (isClientUser, isAdminManager, )

    def get(self, request):
        if not request.GET.get('from_date'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        params = {
            "from_date": request.GET.get('from_date'),
            "to_date": request.GET.get('to_date', datetime.today().strftime('%Y-%m-%d'))
        }

        result = {}

        result['options'] = {}
        result['headers'] = {}
        result['detail'] = []
        result['summary'] = {}
        result['expenses'] = {}

        working_days = WorkingDay.objects.filter(finished=True)
        working_days = apply_filters_by_params(working_days, params)
        # date__range=["2011-01-01", "2011-01-31"]

        result['options']['pagination'] = get_wds_pagination_data(datetime.strptime(params['from_date'], '%Y-%m-%d'))

        result['headers']['cashboxes'] = Cashbox.objects.all().values()
        result['headers']['shift_types'] = ShiftType.objects.all().values()

        result['summary']['income'] = working_days.values("total_income").aggregate(sum=Sum('total_income'))['sum']
        result['summary']['expense'] = 0

        if not working_days:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        start_date = working_days.first().date
        end_date = working_days.last().date

        cashboxes = Cashbox.objects.all()
        shift_types = ShiftType.objects.all()

        # Sample.objects.filter(date__range=["2011-01-01", "2011-01-31"])
        while start_date <= end_date:
            wd = WorkingDay.objects.filter(date=start_date)

            if wd:
                wd = wd[0]

                wd_shifts = Shift.objects.filter(working_day=wd)
                wd_expenses = Expense.objects.filter(working_day=wd, expense_category__is_accounting_expense=True)
                expenses_category = ExpenseCategory.objects.all()

                wd_expenses_sum = wd_expenses.values('sum').aggregate(sum=Sum('sum'))['sum']

                if wd_expenses_sum is not None:
                    result['summary']['expense'] += wd_expenses_sum

                data = {}

                DayL = ['Пн','Вт','Ср','Чт','Пт','Сб','Вс']

                #is_work_day
                data['is_work_day'] = True

                # date
                data['date'] = {}
                data['date']['week'] = DayL[wd.date.weekday()]
                data['date']['day'] = wd.date.day
                data['date']['month'] = wd.date.month
                data['date']['year'] = wd.date.year

                # cash_income
                data['cash_income'] = wd.cash_income

                # noncash_income
                data['noncash_income'] = wd.noncash_income

                # total_income
                data['total_income'] = wd.total_income

                # cash_income
                data['cash_income'] = wd.cash_income

                # total_expenses
                data['total_expenses'] = 0
                if wd_expenses_sum is not None:
                    data['total_expenses'] += wd_expenses_sum

                # expenses
                data['expenses'] = generate_expenses_data(wd_expenses, expenses_category)

                # cashboxes
                data['cashboxes'] = {}
                for cashbox in cashboxes:
                    cashbox_shifts = wd_shifts.filter(cashbox=cashbox.id)
                    cashbox_expenses = wd_expenses.filter(cashbox=cashbox.id)

                    cashbox_cash_income_sum = 0
                    cashbox_noncash_income_sum = 0
                    cashbox_total_income_sum = 0
                    cashbox_cash_refund_sum = 0
                    cashbox_total_expenses_sum = 0

                    cashbox_cash_income = cashbox_shifts.values("cash_income").aggregate(sum=Sum('cash_income'))['sum']
                    cashbox_noncash_income = cashbox_shifts.values("noncash_income").aggregate(sum=Sum('noncash_income'))['sum']
                    cashbox_total_income = cashbox_shifts.values("shift_income").aggregate(sum=Sum('shift_income'))['sum']
                    cashbox_cash_refund = cashbox_shifts.values("cash_refund").aggregate(sum=Sum('cash_refund'))['sum']
                    cashbox_total_expenses = cashbox_expenses.values("sum").aggregate(sum=Sum('sum'))['sum']

                    if cashbox_total_expenses:
                        cashbox_total_expenses_sum = cashbox_total_expenses
                    if cashbox_cash_income:
                        cashbox_cash_income_sum = cashbox_cash_income
                    if cashbox_noncash_income:
                        cashbox_noncash_income_sum = cashbox_noncash_income
                    if cashbox_total_income:
                        cashbox_total_income_sum = cashbox_total_income
                    if cashbox_cash_refund:
                        cashbox_cash_refund_sum = cashbox_cash_refund

                    data['cashboxes'][cashbox.id] = {}
                    data['cashboxes'][cashbox.id]['id'] = cashbox.id
                    data['cashboxes'][cashbox.id]['name'] = cashbox.name
                    data['cashboxes'][cashbox.id]['cash_income'] = cashbox_cash_income_sum
                    data['cashboxes'][cashbox.id]['noncash_income'] = cashbox_noncash_income_sum
                    data['cashboxes'][cashbox.id]['total_income'] = cashbox_total_income_sum
                    data['cashboxes'][cashbox.id]['cash_refund'] = cashbox_cash_refund_sum
                    data['cashboxes'][cashbox.id]['total_expenses'] = cashbox_total_expenses_sum

                    #cashbox expenses
                    data['cashboxes'][cashbox.id]['expenses'] = generate_expenses_data(cashbox_expenses, expenses_category)

                    data['cashboxes'][cashbox.id]['shifts'] = generate_shift_data(cashbox_shifts, shift_types)

                result['detail'].append(data)

            start_date += timedelta(days=1)

        # result['detail'] = add_non_work_days_data(result['detail'], params)

        result['expenses']['shift'] = get_total_expenses_data(working_days)
        result['expenses']['additional'] = get_additional_expenses_data(params, result['summary'])

        result['summary']['expense'] += result['expenses']['additional']['total']
        result['summary']['net_profit'] = result['summary']['income'] - result['summary']['expense']

        return Response(result, status=status.HTTP_200_OK)
