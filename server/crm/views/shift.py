from crm.utils.shift_payroll import update_shift_payroll_data
from crm.utils.shift_tracker import calculate_shift_trackers, is_permissible_traker_action
from crm.utils.cashbox import is_cashbox_active
from crm.utils.common import debug
from crm.utils.datetime import get_today_datetime
from crm.utils.working_day import get_active_working_day, get_last_working_day
from main.models import Employee
from crm.serializers.shift import CloseShiftSerializer, OpenShiftSerializer
from crm.models import Shift, ShiftTraker, WorkingTime
from crm.utils.shift import calculate_shift_fact, get_employee_active_shift
from rest_framework.response import Response
from rest_framework.views import APIView
from crm.permissions import isClientUser, isEmployee
from rest_framework import status
import datetime


class CheckShiftView(APIView):
    permission_classes = (isClientUser, isEmployee, )

    def get(self, request):
        active_wd = get_active_working_day(create=False)
        active_shift = get_employee_active_shift(user=request.user)

        response = {
            "active_wd": True if active_wd else False,
            "active_shift": True if active_shift else False
        }

        return Response(response, status=status.HTTP_200_OK)


class OpenShiftView(APIView):
    permission_classes = (isClientUser, isEmployee, )

    def post(self, request):
        last_wd = get_last_working_day()

        if last_wd:
            if last_wd.finished and last_wd.date == datetime.date.today():
                return Response(
                    {"error_message": "Рабочий день уже завершился, пожалуйста дождитесь началы нового рабочего дня "
                                      "или обратитесь к руководству!"},
                    status=status.HTTP_400_BAD_REQUEST)

        active_wd = get_active_working_day(create=True)
        active_shift = get_employee_active_shift(request.user)

        if active_shift:
            debug("active_shift", "Активная смена уже существует")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ser_data = {
            'working_day': active_wd.id,
            'shift_type': request.data['shift_type'] if "shift_type" in request.data else None,
            'cashbox': request.data['cashbox'] if "cashbox" in request.data else None,
            'employee': Employee.objects.get(user=request.user).id
        }

        serializer = OpenShiftSerializer(data=ser_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if is_cashbox_active(cashbox_id=serializer.validated_data['cashbox']):
            debug("is_cashbox_active", "Данная касса уже занята")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        new_shift = Shift.objects.get(pk=serializer.data['id'])
        new_working_time = WorkingTime.objects.create(shift=new_shift)

        ShiftTraker.objects.create(working_time=new_working_time, action=ShiftTraker.START, datetime=get_today_datetime())

        return Response({"success": True}, status=status.HTTP_201_CREATED)


class ActiveShiftView(APIView):
    permission_classes = (isClientUser,)

    def get(self, request):
        active_shift = get_employee_active_shift(request.user)

        if not active_shift:
            debug("active_shift", "Нет активной смены")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        working_time = WorkingTime.objects.filter(shift=active_shift)

        if working_time is None:
            debug("working_time", "Рабочее время не найдено")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        working_time = working_time[0]

        shift_trackers = ShiftTraker.objects.filter(working_time=working_time).order_by('datetime').values()

        if not len(shift_trackers) >= 1:
            debug("shift_trackers", "Трекеры смен не найдены")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        tracker_times = calculate_shift_trackers(shift_trackers)

        return Response(tracker_times, status=status.HTTP_200_OK)

    def put(self, request):
        active_shift = get_employee_active_shift(request.user)

        if not active_shift:
            debug("active_shift", "Нет активной смены")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        working_time = WorkingTime.objects.filter(shift=active_shift)

        if working_time is None:
            debug("working_time", "Рабочее время не найдено")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        working_time = working_time[0]

        active_shift_tracker = ShiftTraker.objects.filter(working_time=working_time).order_by('datetime').last()

        if not active_shift_tracker:
            debug("last_shift_tracker", "Нет активного трекера")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        last_action = int(active_shift_tracker.action)
        current_action = request.data['action'] if "action" in request.data else None

        if not is_permissible_traker_action(current_action, last_action):
            debug("is_permissible_action", "Недопустимое значение")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if active_shift_tracker.datetime >= get_today_datetime():
            debug("last_shift_tracker.datetime", "Недопустимое значение для времени трекера")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        new_shift_tracker = ShiftTraker.objects.create(working_time=working_time, action=current_action, datetime=get_today_datetime())

        if not new_shift_tracker:
            debug("new_shift_tracker", "Ошибка при создании трекера времени")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        shift_trackers = ShiftTraker.objects.filter(working_time=working_time).order_by('datetime').values()
        tracker_current_time = calculate_shift_trackers(shift_trackers)

        if not tracker_current_time:
            debug("tracker_current_time", "Ошибка при подсчете трекера времени")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(tracker_current_time, status=status.HTTP_200_OK)


class CloseShiftView(APIView):
    permission_classes = (isClientUser,)

    def post(self, request):
        active_shift = get_employee_active_shift(request.user)

        if not active_shift:
            debug("active_shift", "Нет активной смены")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ser_data = {
            'cash_start': request.data['cash_start'] if "cash_start" in request.data else None,
            'cash_end': request.data['cash_end'] if "cash_end" in request.data else None,
            'noncash_start': request.data['noncash_start'] if "noncash_start" in request.data else None,
            'noncash_end': request.data['noncash_end'] if "noncash_end" in request.data else None,
            'sales': request.data['sales'] if "sales" in request.data else None,
            'cashbox_fact': request.data['cashbox_fact'] if "cashbox_fact" in request.data else None,
            'cash_refund': request.data['cash_refund'] if "cash_refund" in request.data else None,
            'noncash_refund': request.data['noncash_refund'] if "noncash_refund" in request.data else None,
            'difference_report': request.data[
            'difference_report'] if "difference_report" in request.data else None, 'finished': True
        }

        serializer = CloseShiftSerializer(instance=active_shift, data=ser_data)
        if not serializer.is_valid():
            return Response({"error_fields":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        calculated_shift_data = calculate_shift_fact(active_shift, serializer.validated_data)

        if not calculated_shift_data['fact']:
            if not serializer.validated_data['difference_report']:
                result = {'success': False}
                result.update(calculated_shift_data)
                return Response(result, status=status.HTTP_200_OK)

        ser_data.update(calculated_shift_data)

        serializer = CloseShiftSerializer(instance=active_shift, data=ser_data)
        if not serializer.is_valid():
            return Response({"error_fields": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        working_time = WorkingTime.objects.filter(shift=active_shift)

        if working_time is None:
            debug("working_time", "Рабочее время не найдено")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        working_time = working_time[0]

        ShiftTraker.objects.create(working_time=working_time, action=ShiftTraker.STOP, datetime=get_today_datetime())

        tracker_times = calculate_shift_trackers(ShiftTraker.objects.filter(working_time=working_time).order_by('datetime').values())

        working_time.work_time = tracker_times['work_time']
        working_time.break_time = tracker_times['break_time']
        working_time.save()

        update_shift_payroll_data(active_shift, working_time.work_time)

        result = {'success': True}
        result.update()
        return Response(result, status=status.HTTP_200_OK)
