from django.db import models
from crm.utils.common import debug
from crm.models import Cashbox, Expense, ExpenseCategory, Shift, ShiftType, WorkingDay
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isAdminManager, isClientUser
from rest_framework import status
from calendar import monthrange
from datetime import date, timedelta
from django.db.models import Sum
from django.db.models import F


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


class AccountingView(APIView):
    permission_classes = (isClientUser, isAdminManager, )

    def get(self, request):

        result = {}
        
        result['headers'] = {}
        result['detail'] = []
        result['summary'] = {}

        working_days = WorkingDay.objects.filter(finished=True).order_by('date')

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

        while start_date <= end_date:
            wd = WorkingDay.objects.filter(date=start_date)

            if not wd:
                result['detail'].append(None)
            else:
                wd = wd[0]

                wd_shifts = Shift.objects.filter(working_day=wd)
                wd_expenses = Expense.objects.filter(working_day=wd, expense_category__is_accounting_expense=True)
                expenses_category = ExpenseCategory.objects.all()

                result['summary']['expense'] += wd_expenses.values('sum').aggregate(sum=Sum('sum'))['sum']

                data = {}

                DayL = ['Пн','Вт','Ср','Чт','Пт','Сб','Вс']

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
                data['total_expenses'] = wd_expenses.values('sum').aggregate(sum=Sum('sum'))['sum']

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

                    #expenses
                    data['cashboxes'][cashbox.id]['expenses'] = generate_expenses_data(cashbox_expenses, expenses_category)

                    #expenses
                    data['cashboxes'][cashbox.id]['shifts'] = generate_shift_data(cashbox_shifts, shift_types)

                result['detail'].append(data)

            start_date += timedelta(days=1)

            result['summary']['net_profit'] = result['summary']['income'] - result['summary']['expense']

        return Response(result, status=status.HTTP_200_OK)
