import calendar
import time
from datetime import timedelta, datetime, date
import math

def get_current_datetime_string():
    """
    Returns the current date and time as a string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return get_current_datetime_formatted('%Y-%m-%d %H:%M:%S')

def get_current_datetime_formatted(format):
    """
    Returns the current date and time as a string in a specified format.
    """
    return format_timestamp(time.time(), format)

def timestamp_to_datetime_string(timestamp):
    """
    Converts a timestamp to a datetime string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return format_timestamp(timestamp, "%Y-%m-%d %H:%M:%S")

def format_timestamp(timestamp, format):
    """
    Formats a given timestamp to a datetime string using the specified format.
    """
    local_time = time.localtime(int(timestamp))
    return time.strftime(format, local_time)

def datetime_string_to_timestamp(dateStr):
    """
    Converts a datetime string in 'YYYY-MM-DD HH:MM:SS' format to a timestamp.
    """
    return time.mktime(time.strptime(dateStr, '%Y-%m-%d %H:%M:%S'))

def datetime_string_to_timestamp_custom_format(dateStr, format):
    """
    Converts a datetime string in a custom format to a timestamp.
    """
    return time.mktime(time.strptime(dateStr, format))

def get_current_date_components():
    """
    Returns the current year, month, and day as integers.
    """
    curTime = datetime.now()
    return curTime.year, curTime.month, curTime.day

def get_date_after_days(days):
    """
    Returns the date string 'YYYY-MM-DD' for a date a specified number of days from today.
    """
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

def datestring_to_date(date_str):
    """
    Converts a date string 'YYYY-MM-DD' to a datetime.date object.
    """
    return date(*map(int, date_str.split('-')))

def datetime_to_timestamp(datetime_obj):
    """
    Converts a datetime object to a timestamp.
    """
    return datetime_string_to_timestamp(datetime_obj.strftime("%Y-%m-%d %H:%M:%S"))

def get_current_weekday():
    """
    Returns the current weekday as an integer (Monday=1, Sunday=7).
    """
    return datetime.now().weekday() + 1

def get_week_number_in_month(year, month, day):
    """
    Calculates the week number of a specific day within its month.
    """
    end = int(datetime(year, month, day).strftime("%W"))
    begin = int(datetime(year, month, 1).strftime("%W"))
    return end - begin + 1

def datetime_to_string(datetime_obj, format="%Y-%m-%d %H:%M:%S"):
    """
    Converts a datetime object to a string. Uses a default format 'YYYY-MM-DD HH:MM:SS' or a custom format if provided.
    """
    return datetime_obj.strftime(format)

def datetime_to_date_string(datetime_obj):
    """
    Converts a datetime object to a date string 'YYYY-MM-DD'. Returns an empty string for invalid input.
    """
    if not datetime_obj:
        return ''
    if isinstance(datetime_obj, str):
        return datetime_obj
    return datetime_obj.strftime("%Y-%m-%d")

def calculate_minute_difference(time_one, time_two):
    """
    Calculates the difference in minutes between two time strings 'HH:MM:SS' of the same day.
    """
    now_date_str = datetime.now().strftime("%Y-%m-%d")
    timestamp_one = datetime_string_to_timestamp(f"{now_date_str} {time_one}")
    timestamp_two = datetime_string_to_timestamp(f"{now_date_str} {time_two}")
    return math.ceil((int(timestamp_two) - int(timestamp_one)) / 60)

def get_current_week_dates():
    """
    Returns the start and end dates of the current week.
    """
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

def get_dates_between(start_day, end_day):
    """
    Generates a list of date strings 'YYYY-MM-DD' between two specified dates.
    """
    date_list = []
    begin_date = datetime.strptime(start_day, "%Y-%m-%d")
    end_date = datetime.strptime(end_day, "%Y-%m-%d")
    while begin_date <= end_date:
        date_list.append(begin_date.strftime("%Y-%m-%d"))
        begin_date += timedelta(days=1)
    return date_list

def get_day_difference(start_day, end_day):
    """
    Calculates the number of days between two dates.
    """
    start_date = datetime.strptime(start_day, "%Y-%m-%d")
    end_date = datetime.strptime(end_day, "%Y-%m-%d")
    return (end_date - start_date).days

def get_date_sequence(start_day, number, forward=True):
    """
    Generates a list of date strings 'YYYY-MM-DD' starting from a given date, for a specified number of days.
    Direction can be forward (True) or backward (False).
    """
    date_list = []
    begin_date = datetime.strptime(start_day, "%Y-%m-%d")
    for _ in range(number):
        date_list.append(begin_date.strftime("%Y-%m-%d"))
        begin_date += timedelta(days=1 if forward else -1)
    return date_list

def get_start_end_of_week(day):
    """
    Returns the start and end date strings 'YYYY-MM-DD' of the week for a given date.
    """
    start_day = day - timedelta(days=day.weekday())
    end_day = start_day + timedelta(days=6)
    return start_day.strftime("%Y-%m-%d"), end_day.strftime("%Y-%m-%d")
