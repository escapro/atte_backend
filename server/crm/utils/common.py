from django.db.models.aggregates import Sum
from rest_framework import status
from rest_framework.response import Response
from atte.constans import ADMIN, CLIENT, EMPLOYEE, MANAGER
from main.models import Admin, Employee, Manager
from crm.models import Shift, ShiftType

def getSubdomain(request):
    return request.META['HTTP_HOST'].split('.')[0]

def getUserClientInfo(user):
    result = {}
    result['role'] = ''
    result['client'] = []

    employee = Employee.objects.filter(user=user)

    # user is employee
    if employee:
        result['role'] = EMPLOYEE
        result['client'] = employee[0].client.name
    else:
        manager = Manager.objects.filter(user=user)

        # user is manager
        if manager:
            result['role'] = MANAGER
            clients = getattr(manager[0], CLIENT).all().values('name')
            result['client'] = [client['name'] for client in clients]
        else:
            admin = Admin.objects.filter(user=user)

            # user is manager
            if admin:
                result['role'] = ADMIN
                clients = getattr(admin[0], CLIENT).all().values('name')
                result['client'] = [client['name'] for client in clients]

    return result


def check_working_day_for_completness(working_day):
    shifts = Shift.objects.filter(working_day=working_day)
    last_shiftType = ShiftType.objects.filter(is_active=True).order_by('index').last()
    
    if shifts.last().shift_type.index == last_shiftType.index:
        working_day.cash_income = shifts.aggregate(Sum('cash_income'))['cash_income__sum']
        working_day.noncash_income = shifts.aggregate(Sum('noncash_income'))['noncash_income__sum']
        working_day.total_income = working_day.cash_income + working_day.noncash_income
        working_day.finished = True
        working_day.save()


def debug(title: str, text: str):
    print()
    print("{}: {}".format(title, text))
    print()