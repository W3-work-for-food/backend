from datetime import datetime, timedelta


def read_notifications_for_month():
    """
    Возвращает прочитанные уведомления за последний месяц.
    """
    today = datetime.now().date()
    last_month = today - timedelta(days=30)
    return last_month, today

def name_choices(value, choise):
    """Выбор из choice."""
    for name_full, name_short in choise:
        if value == name_short:
            return name_full
