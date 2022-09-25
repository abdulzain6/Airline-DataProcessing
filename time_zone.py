from datetime import datetime, timedelta

weekdays = {
    "M" : 0,
    "T" : 1,  
    "W" : 2,
    "Th" : 3, 
    "F" : 4,
    "Sa" : 5,
    "Su" : 6,
}


    # https://stackoverflow.com/questions/16769902/finding-the-date-of-the-next-saturday
def get_next_weekday(weekday_number, time_zone):
    """
    @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
    """
    assert 0 <= weekday_number <= 6

    today_date = datetime.now(time_zone)
    next_week_day = timedelta((7 + weekday_number - today_date.weekday()) % 7)
    return today_date + next_week_day


def time_between_given_date_and_next_weekday(weekday, time, time_zone):

    weekday_date = get_next_weekday(weekday, time_zone)
    return weekday_date.date() - time