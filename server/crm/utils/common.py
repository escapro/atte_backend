from atte.constans import ADMIN, CLIENT, EMPLOYEE, MANAGER
from main.models import Admin, Employee, Manager
from django.db import connection


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
