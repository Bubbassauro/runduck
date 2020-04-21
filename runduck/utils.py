"""General helper functions"""
import re
import dateutil.parser
import croniter
from datetime import datetime
from cron_descriptor import get_description


def get_object_property(obj, property_list, default=None):
    """Safely traverse an object to find nested properties, returns None if property doesn't exist.
    Does not throw errors if any property in the path doesn't exist.
    Separate properties in property_list by dot, for example:
        get_object_property(my_object, 'child_property.grandchild_property')
    """
    properties = property_list.split(".")
    if obj:
        for prop in properties:
            if prop in obj:
                obj = obj[prop]
            else:
                return default
    return obj


def get_elapsed_time(start_date, end_date):
    """Format elapsed time between start date and end date
    
    :param start_date: Start date
    :type start_date: string
    :param end_date: End Date
    :type end_date: string
    """
    start = dateutil.parser.parse(start_date)
    end = dateutil.parser.parse(end_date)
    elapsed = str(end - start)

    # try to get pieces to format for humans
    matches = re.search("(?P<hours>\d+)(:?)(?P<minutes>\d+):(?P<seconds>\d+)$", elapsed)
    if not matches:
        return elapsed

    hms = matches.groupdict()
    formatted = ""
    if int(hms["hours"]) > 0:
        formatted = f"{hms['hours']}h "
    formatted = f"{formatted}{hms['minutes']}m {hms['seconds']}s"
    return formatted


def get_cron(schedule):
    if not schedule:
        return ""

    minute, hour, seconds, dayofmonth, month, weekday = "*", "*", "*", "*", "*", "*"
    if schedule.get("time"):
        if schedule["time"].get("minute"):
            minute = schedule["time"]["minute"]
            # format in a way that croniter understands
            minute = re.sub(r",$", "", minute)  # "0," -> "0"
            minute = re.sub(r"^0{,1}/", "*/", minute)  # "0/5" or "/5" -> "*/5"

        if schedule["time"].get("hour"):
            hour = schedule["time"]["hour"]
        if schedule["time"].get("seconds"):
            seconds = schedule["time"]["seconds"]

    if schedule.get("month"):
        month = schedule["month"]

    if schedule.get("dayofmonth"):
        if schedule["dayofmonth"]["day"]:
            dayofmonth = schedule["dayofmonth"]["day"]

    if schedule.get("weekday"):
        if schedule["weekday"].get("day"):
            weekday = schedule["weekday"]["day"]

    cron = f"{minute} {hour} {dayofmonth} {month} {weekday}"
    return cron


def get_next_execution(cron):
    """Get next execution as ISO date"""
    if not cron:
        return None

    cron = croniter.croniter(cron, datetime.now())
    nextdate = cron.get_next(datetime)
    return nextdate.isoformat()
