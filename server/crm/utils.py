from main.models import Admin, Employee, Manager
from django.db import connection


def getSubdomain(request):
    return request.META['HTTP_HOST'].split('.')[0]


def getUserClientInfo(user):
    result = {}
    result['role'] = ''
    result['client'] = []

    employee = Employee.objects.filter(user=user)

    if not employee:
        managers = Manager.objects.filter(user=user)
        if not managers:
            admin = Admin.objects.filter(user=user)
            if admin:
                result['role'] = 'admin'
        else:
            if managers:
                result['role'] = 'manager'

                for manager in managers:
                    result['client'].append(manager.client.name)
    else:
        result['client'] = None
        employee = employee[0]
        result['client'] = employee.client.name
        result['role'] = 'employee'

    return result
