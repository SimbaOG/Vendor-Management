from datetime import datetime as dt
from datetime import timedelta as td
from zoneinfo import ZoneInfo

from django.conf import settings


def valid_upto_date() -> dt:
    """
    This function is a helper utility function which is used to calculate the expiry date time of the token.
    It depends on `TOKEN_MAX_EXPIRY` settings in the configuration to calculate that. DO NOT ALTER/REMOVE THIS FUNCTION
    :return:
    """

    num_seconds = settings.TOKEN_MAX_EXPIRY
    crr_time = dt.now(tz=ZoneInfo('Asia/Kolkata'))

    valid_upto = crr_time + td(seconds=num_seconds)
    return valid_upto
