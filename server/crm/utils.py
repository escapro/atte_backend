from atte.constans import ADMIN, EMPLOYEE, MANAGER
from main.models import Admin, Employee, Manager
from django.db import connection


def getSubdomain(request):
    return request.META['HTTP_HOST'].split('.')[0]


def getUserClientInfo(user):
    result = {}
    result['role'] = ''
    result['clients'] = []

    employee = Employee.objects.filter(user=user)

    if not employee:
        manager = Manager.objects.filter(user=user)
        if not manager:
            admin = Admin.objects.filter(user=user)
            if admin:
                result['role'] = ADMIN
        else:
            if manager:
                result['role'] = MANAGER

                for m in manager:
                    result['clients'].append(m.client.name)
    else:
        result['role'] = EMPLOYEE

        for e in employee:
            result['clients'].append(e.client.name)

    return result
