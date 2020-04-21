"""General helper functions"""
import re
import dateutil.parser


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
