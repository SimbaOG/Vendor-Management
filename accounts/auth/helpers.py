from datetime import datetime as dt
from datetime import timedelta as td
from zoneinfo import ZoneInfo

from django.conf import settings


def valid_upto_date():
    num_seconds = settings.TOKEN_MAX_EXPIRY
    crr_time = dt.now(tz=ZoneInfo('Asia/Kolkata'))

    valid_upto = crr_time + td(seconds=num_seconds)
    return valid_upto
