from datetime import datetime as dt
from typing import Union

import yaml


def yaml_coerce(value):
    """
    This function is used to convert a dictionary string literal to a dictionary object.
    :param value:
    :return:
    """
    if isinstance(value, str):
        return yaml.load(f'dummy: {value}', Loader=yaml.SafeLoader)['dummy']

    return value


def string_to_datetime(date_string: str) -> Union[dt, None]:
    try:
        date_time = dt.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return None
    return date_time
