from datetime import datetime

UTC_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def to_camel_case(field_name):
    """Transform a snake_case field to a camelCase field
    :param field_name:
    :return: a camelCase field
    """
    name_parts = field_name.split("_")
    camel_case = "".join(char.capitalize() for char in name_parts[1:])
    camel_case = name_parts[0] + camel_case
    return camel_case


def get_current_utc():
    """Get the current time in UTC with the format used by the api in the Date
     HTTP Header.
    :return: current time in UTC
    :rtype: str
    """
    return datetime.utcnow().strftime(UTC_STRING_FORMAT)


def datetime_isoformat(datetime_object):
    """Return a date in a iso format expected from the api.
    :return: a date in an iso format
    :rtype: str
    """
    return datetime_object.strftime(DATETIME_FORMAT)
