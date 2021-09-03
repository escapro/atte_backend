from django.db.models.query import QuerySet
from crm.models import ShiftTraker
from typing import Optional
import datetime
import math

def is_permissible_traker_action(current_action: int, last_action: int) -> bool:
    """
    Определяет, разрашено ли указанное действие
    
    :param int current_action: Идентификатор текущего действия
    :param int last_action: Идентификатор предыдущего действия
    """

    result = True

    if current_action == ShiftTraker.START or current_action == ShiftTraker.STOP:
        result = False

    if last_action == ShiftTraker.START:
        if current_action == ShiftTraker.START or current_action == ShiftTraker.RESUME:
            result = False
    elif last_action == ShiftTraker.PAUSE:
        if current_action == ShiftTraker.START or current_action == ShiftTraker.PAUSE:
            result = False
    elif last_action == ShiftTraker.RESUME:
        if current_action == ShiftTraker.START or current_action == ShiftTraker.RESUME:
            result = False

    return result


def calculate_shift_trackers(shift_trackers: QuerySet) -> Optional[dict]:
    """
    Подсчитывает рабочее время, перерывное время и текущее действие (START, PAUSE, RESUME, STOP) в смене
    
    :param QuerySet shift_trackers: Объект трекеров, которые нужно подсчитать
    """

    if not shift_trackers[0]['action'] == ShiftTraker.START:
        return None

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