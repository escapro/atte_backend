from crm.serializers.shift import ShiftSerializer
from crm.models import Shift, ShiftTraker, WorkingDay
from django.forms.models import model_to_dict
import datetime
import math
import pytz    
from django.utils import timezone

def get_exist_active_shift(request):
    result = {
        "exist": False,
        "active_wd": False,
        "is_current_user": False,
        "shift": None
    }

    last_working_day = WorkingDay.objects.all().order_by('date').last()

    if last_working_day:
        if not last_working_day.finished:
            result["active_wd"] = True
            last_shift = Shift.objects.filter(working_day=last_working_day).last()
            if last_shift:
                if not last_shift.finished:
                    result["exist"] = True
                    result["shift"] = ShiftSerializer(last_shift).data
                    if last_shift.employee.user == request.user:
                        result["is_current_user"] = True

    return result

def calculate_shift_trackers(shift_trackers):
    if not shift_trackers[0]['action'] == ShiftTraker.START:
        return False

    data = {
        "work_time": 0,
        "break_time": 0,
        "current_action": shift_trackers[len(shift_trackers) - 1]['action']
    }

    for index, tracker in enumerate(shift_trackers):
        current_action = tracker['action']

        # START
        if current_action == ShiftTraker.START:
            next_index = index + 1
            if next_index < len(shift_trackers):
                next_tracker = shift_trackers[next_index]
                # START -> STOP
                if next_tracker['action'] == ShiftTraker.STOP:
                    data['work_time'] += math.ceil((next_tracker['datetime'] - tracker['datetime']).total_seconds())
                # START -> PAUSE
                elif next_tracker['action'] == ShiftTraker.PAUSE:
                    data['work_time'] += math.ceil((next_tracker['datetime'] - tracker['datetime']).total_seconds())
            # START -> ''
            else:
                data['work_time'] += math.ceil((datetime.datetime.now() - tracker['datetime'].replace(tzinfo=None)).total_seconds())
        # PAUSE
        elif current_action == ShiftTraker.PAUSE:
            next_index = index + 1
            if next_index < len(shift_trackers):
                next_tracker = shift_trackers[next_index]
                # PAUSE -> RESUME                                                                                                                                                                                                              -> RESUME
                if next_tracker['action'] == ShiftTraker.RESUME:
                    data['break_time'] += math.ceil((next_tracker['datetime'] - tracker['datetime']).total_seconds())
                # PAUSE -> STOP
                elif next_tracker['action'] == ShiftTraker.STOP:
                    data['break_time'] += math.ceil((next_tracker['datetime'] - tracker['datetime']).total_seconds())
            # PAUSE -> ''
            else:
                data['break_time'] += math.ceil((datetime.datetime.now() - tracker['datetime'].replace(tzinfo=None)).total_seconds())
        # RESUME
        elif current_action == ShiftTraker.RESUME:
            next_index = index + 1
            if next_index < len(shift_trackers):
                next_tracker = shift_trackers[next_index]
                # RESUME -> PAUSE
                if next_tracker['action'] == ShiftTraker.PAUSE:
                    data['work_time'] += math.ceil((next_tracker['datetime'] - tracker['datetime']).total_seconds())
                # RESUME -> STOP
                elif next_tracker['action'] == ShiftTraker.STOP:
                    data['work_time'] += math.ceil((next_tracker['datetime'] - tracker['datetime']).total_seconds())
            # RESUME -> ''
            else:
                data['work_time'] += math.ceil((datetime.datetime.now() - tracker['datetime'].replace(tzinfo=None)).total_seconds())

    return data