from datetime import datetime, timedelta


def read_notifications_for_month():
    """
    Возвращает прочитанные уведомления за последний месяц.
    Returns:
        tuple: Кортеж с начальной и конечной датами диапазона.
    """
    today = datetime.now().date()
    last_month = today - timedelta(days=30)
    return last_month, today
