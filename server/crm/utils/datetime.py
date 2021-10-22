import datetime


def get_today_datetime():
    """
    Возвращает сегоднящнюю дату и время
    """
    return datetime.datetime.fromisoformat(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))


def format_with_zero(value: int) -> str:
    """
    Добавляет начальные нули к элементу дате
    """
    return str(value) if value>=10 else "0{}".format(value)