from datetime import datetime


def check_date(date_to_check):
    today = datetime.today()
    try:
        return datetime.strptime(date_to_check, '%Y-%m-%d').date() >= datetime.today().date()
    except ValueError:
        pass
    try:
        return datetime.strptime(date_to_check, '%Y-%m') >= datetime(year=today.year, month=today.month, day=1)
    except ValueError:
        return False


def format_date(date_to_format):
    return datetime.fromisoformat(date_to_format)
