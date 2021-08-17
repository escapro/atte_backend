from django.db.models.aggregates import Sum
from atte.constans import ADMIN, CLIENT, EMPLOYEE, MANAGER
from main.models import Admin, Employee, Manager
from crm.models import Shift, ShiftType, WorkingDay
import datetime


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


def check_working_day():
    result = {
        'success': False,
        'object': None,
        'message': None
    }

    last_working_day = WorkingDay.objects.all().order_by('date').last()
    last_working_day_shifts = Shift.objects.filter(working_day=last_working_day)
    shift_types = ShiftType.objects.filter(is_active=True)

    if last_working_day.finished:
        if datetime.date.today() == last_working_day.date:
            result['message'] = "Рабочий день уже завершился, пожалуйста дождитесь началы нового рабочего дня или обратитесь к руководству!"
        else:
            new_working_day = WorkingDay.objects.create(date=datetime.date.today())
            result['success'] = True
            result['object'] = new_working_day
    else:
        result['success'] = True
        result['object'] = last_working_day

    return result

    # def newWorkingDay():
    #     if datetime.date.today() == last_working_day.date:
    #         result['message'] = "Рабочий день уже завершился, пожалуйста дождитесь началы нового рабочего дня или обратитесь к руководству!"
    #     else:
    #         new_working_day = WorkingDay.objects.create(date=datetime.date.today())
    #         result['success'] = True
    #         result['object'] = new_working_day

    # if last_working_day.finished:
    #     newWorkingDay()
    # else:
    #     if last_working_day_shifts.count() == shift_types.count():
    #         last_working_day.finished = True
    #         last_working_day.save()
    #         newWorkingDay()
    #     else:
    #         result['success'] = True
    #         result['object'] = last_working_day

    # return result


def check_working_day_for_completness(working_day):
    shifts = Shift.objects.filter(working_day=working_day)
    last_shiftType = ShiftType.objects.filter(is_active=True).order_by('index').last()
    
    if shifts.last().shift_type.index == last_shiftType.index:
        working_day.cash_income = shifts.aggregate(Sum('cash_income'))['cash_income__sum']
        working_day.noncash_income = shifts.aggregate(Sum('noncash_income'))['noncash_income__sum']
        working_day.total_income = working_day.cash_income + working_day.noncash_income
        working_day.finished = True
        working_day.save()