from datetime import datetime

UTC_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"


def to_camel_case(field_name):
    name_parts = field_name.split("_")
    camel_case = "".join(char.capitalize() for char in name_parts[1:])
    camel_case = name_parts[0] + camel_case
    return camel_case


def get_current_utc():
    """Get the current time in UTC with the format used by the api in the Date
     HTTP Header.
    @return current time in UTC
    @rtype str
    """
    return datetime.utcnow().strftime(UTC_STRING_FORMAT)
