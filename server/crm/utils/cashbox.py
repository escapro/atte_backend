from crm.utils.shift import get_active_shifts


def is_cashbox_active(cashbox_id: int = None) -> bool:
    """
    Определяет, не занята ли указанная касса

    :param int cashbox_id: Идентификатор кассы
    """

    is_active = False

    active_shifts = get_active_shifts()

    if active_shifts:
        if active_shifts.filter(cashbox=cashbox_id):
            is_active = True

    return is_active
