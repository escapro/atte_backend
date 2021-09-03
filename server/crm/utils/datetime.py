
import datetime


def get_today_datetime():
    """
    Возвращает сегоднящнюю дату и время
    """
    return datetime.datetime.fromisoformat(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))