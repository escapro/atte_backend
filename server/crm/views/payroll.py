from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.models import ShiftPayrollPeriod, ShiftPayroll
from crm.permissions import isAdminManager, isClientUser
from crm.serializers.shift_payroll_period import ShiftPayrollPeriodSerializer
from crm.utils.common import debug
from crm.utils.shift_payroll_period import format_payroll_period
from main.models import Employee
from main.serializers.employee import EmployeeSerializerOnlyUser


def get_periods_data(employee, periods, month, year):
    result = {}

    for period in periods:
        payroll = ShiftPayroll.objects.filter(shift__employee=employee,
                                              period=period,
                                              shift__working_day__date__month=month,
                                              shift__working_day__date__year=year)
        
        key_name = format_payroll_period(period.day, int(month), int(year))

        result[key_name] = {
            "from_shift": payroll.values("from_shift").aggregate(sum=Sum('from_shift'))['sum'] if payroll.exists() else 0,
            "from_interest": payroll.values("from_interest").aggregate(sum=Sum('from_interest'))['sum'] if payroll.exists() else 0,
        }

        # if payroll.exists():
        #     result[key_name]['from_shift'] = payroll.values("from_shift").aggregate(sum=Sum('from_shift'))['sum']
        # else:
        #     result[key_name]['from_shift'] = 0

    return result


def get_headers_data(payroll_dates, month, year):
    result = []

    debug('payroll_dates', payroll_dates)

    for period in payroll_dates:
        date = '{}.{}.{}'.format(format_payroll_period(period.day, int(month), int(year)), month, year)
        result.append([
            'За смены: {}'.format(date),
            'Проценты: {}'.format(date),
            'Суммарно: {}'.format(date),
            'Выплачено: {}'.format(date),
        ])

    return result


class PayrollView(APIView):
    permission_classes = (isClientUser, isAdminManager)

    def get(self, request):
        if not request.GET.get('date_month') or not request.GET.get('date_year'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        params = {
            "date_month": request.GET.get('date_month'),
            "date_year": request.GET.get('date_year')
        }

        employees = Employee.objects.filter(client=request.tenant)
        employee_serializer = EmployeeSerializerOnlyUser(employees, many=True)

        payroll_dates = ShiftPayrollPeriod.objects.filter(is_active=True)
        payroll_period_serializer = ShiftPayrollPeriodSerializer(payroll_dates, many=True)

        # payrolls = Payroll.objects.filter(date__month=params['date_month'], date__year=params['date_year'])
        # payroll_serializer = PayrollSerializer(payrolls, many=True)

        payrolls = []

        for employee in employees:
            payrolls.append({
                'employee': employee.user.first_name,
                'periods': get_periods_data(employee, payroll_dates, params['date_month'], params['date_year'])
            })

        result = {
            # 'employees': employee_serializer.data,
            # 'payroll_dates': payroll_period_serializer.data,
            'headers': get_headers_data(payroll_dates, params['date_month'], params['date_year']),
            'payrolls': payrolls
        }

        return Response(result, status=status.HTTP_200_OK)
