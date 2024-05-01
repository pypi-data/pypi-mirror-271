from datetime import date, timedelta


def get_last_day_of_month(year: int, month: int):
    if month == 12:
        last_day_of_month = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day_of_month = date(year, month + 1, 1) - timedelta(days=1)
    return last_day_of_month


def get_initial_date_of_monthly_calendar(year: int, month: int):
    first_day_of_month = date(year, month, 1)
    week_of_first_day = first_day_of_month.isocalendar().week
    if first_day_of_month.weekday() != 6:
        week_of_first_day -= 1
        if week_of_first_day == 0:
            week_of_first_day = 52
            year -= 1
    initial_date = date.fromisocalendar(year, week_of_first_day, 7)
    return initial_date


def get_final_date_of_monthly_calendar(year: int, month: int):
    last_day_of_month = get_last_day_of_month(year, month)
    week_of_last_day = last_day_of_month.isocalendar().week
    if last_day_of_month.weekday() == 6:
        week_of_last_day += 1
        if week_of_last_day == 53:
            week_of_last_day = 1
            year += 1
    final_date = date.fromisocalendar(year, week_of_last_day, 6)
    return final_date
