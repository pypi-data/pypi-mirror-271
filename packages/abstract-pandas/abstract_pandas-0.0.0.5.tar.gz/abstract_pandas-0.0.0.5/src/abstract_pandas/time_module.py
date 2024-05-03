import os,time
from datetime import datetime, timedelta
from abstract_utilities import is_number,make_list
def all_combinations_of_strings(strings):
    """
    Generate all possible combinations of the input strings.
    Each combination is a concatenation of the input strings in different orders.

    :param strings: A list of strings for which we want to generate all combinations.
    :return: A list of strings representing all possible combinations.
    """
    from itertools import permutations

    # Generate all permutations of the input list
    all_perms = permutations(strings)

    # Concatenate strings in each permutation to form the combinations
    combinations = [''.join(perm) for perm in all_perms]

    return combinations
def all_date_formats():
    date_formats=[]
    for part in all_combinations_of_strings(list("Ymd")):
        for seperator in ['/','-','_']:
            date_range='%'
            for piece in list(str(part)):
                date_range+=f"{piece}{seperator}%"
            for times in ["%H:%M:%S.%f","%H:%M:%S"]:
                date_format = f"{date_range[:-2]} {times}"
                if date_format not in date_formats:
                    date_formats.append(date_format)
    return date_formats

def get_time_string(data):
    strin = 0
    for string in ["Timestamp","Data_Time_Stamp"]:
        strings = data.get(string)
        if strin:
            pass
    return strings
def convert_date_to_timestamp(date_string,date_format=[]):
    date_formats = all_date_formats()
    date_string = str(date_string)
    date_formats = make_list(date_format)+date_formats
    for date_format in date_formats:
        try:
            date_object = datetime.strptime(date_string, date_format)
            return date_object.timestamp()
        except ValueError:
            continue
    print(f"Date format not recognized: {date_string}")
    return None
def get_rounded_hour_datetime(timeStamp=None,hours=0):
    """
    Returns the current datetime rounded down to the nearest hour,
    with an optional adjustment by a specified number of hours.
    
    :param hours: Number of hours to adjust the rounded datetime by.
                  Defaults to 0 (no adjustment).
    :return: A datetime object for the adjusted, rounded-down hour.
    """
    now = get_convert_timestamp_to_datetime(timeStamp or datetime.now())
    # Round down to the nearest hour
    rounded_hour = now.replace(minute=0, second=0, microsecond=0)
    # Adjust by the specified number of hours
    adjusted_datetime = rounded_hour + timedelta(hours=hours)
    return adjusted_datetime

def get_current_time_with_delta(days=0, hours=0, minutes=0, seconds=0,milliseconds=0):
    # Get the current datetime
    current_time = get_time_stamp()

    # Create a timedelta with the specified duration
    delta = timedelta(days=days, hours=hours, minutes=minutes,seconds=seconds, milliseconds=milliseconds)
    
    # Add the delta to the current time
    new_time = current_time + delta
    
    return new_time
def get_time_stamp():
    return datetime.now()

def get_time_stamp_now():
    return datetime.datetime.now()
    
def get_timestamp():
    return time.time()

def get_hours_ago_datetime(hours=1):
    return get_time_stamp() - get_time_delta_hour(hours=hours)

def get_hours_ago(hours=1):
    hours_ago = get_hours_ago_datetime(hours=1)
    return hours_ago.timestamp()

def get_daily_output(timeStamp=None):
    timeStamp = get_convert_timestamp_to_datetime(convert_date_to_timestamp(timeStamp or get_time_stamp()))
    return timeStamp.strftime('%m-%d-%Y')

def get_hourly_output(timeStamp=None):
    timeStamp = get_convert_timestamp_to_datetime(convert_date_to_timestamp(timeStamp or get_time_stamp()))
    return timeStamp.strftime('%H') + '00'

def get_hour_time_stamp(hours=0):
    return convert_date_to_timestamp(f"{get_rounded_hour_datetime(hours=hours)}")

def get_variable_time_stamp(days=0,hours=0,minutes=0,seconds=0):
    return convert_date_to_timestamp(f"{get_daily_output()} 0:0:00")+(days*(60*60*24))+(hours*(60*60))+(minutes*60)+seconds

def get_variable_datetime(days=0,hours=0,minutes=0,seconds=0):
    timeStamp = get_variable_time_stamp(days=0,hours=0,minutes=0,seconds=0)
    return get_convert_timestamp_to_datetime(timeStamp)
def get_convert_datetime_to_timeStamp(timeStamp):
    timeStamp = timeStamp or get_timestamp()
    if not is_number(timeStamp):
        timeStamp = convert_date_to_timestamp(timeStamp)
    return timeStamp
def get_convert_timestamp_to_datetime(timeStamp=None):
    timeStamp = timeStamp or get_time_stamp()
    if is_number(timeStamp):
        timeStamp = datetime.fromtimestamp(timeStamp)
    return timeStamp
def is_within_day(timeStamp):
    return is_between_range(get_convert_timestamp(timeStamp),get_day_time_stamp(),get_day_time_stamp(days=1))
def is_within_hour(timeStamp):
    return is_between_range(get_convert_timestamp(timeStamp),get_hour_time_stamp(),get_hour_time_stamp(hours=1))

def is_between_range(target,start,end):
    if target >= start and target <=end:
        return True
    return False
def get_creation_time_of_file(file_path):
    if os.path.isfile(file_path):
        creation_time = os.path.getctime(file_path)
        return datetime.datetime.fromtimestamp(creation_time)


