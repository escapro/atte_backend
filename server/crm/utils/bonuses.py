from crm.models import ShiftType, Bonuses
from crm.utils.common import debug


def get_bonus_rate(shift_type: ShiftType, revenue):

    bonuses = Bonuses.objects.filter(shift_type=shift_type).order_by('-revenue_to')
    rate = 0

    for bonus in bonuses:
        if revenue >= bonus.revenue_to:
            rate = bonus.rate
            break

    return rate
