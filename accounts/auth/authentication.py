from datetime import datetime as dt
from zoneinfo import ZoneInfo

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import TokenManager


class UserAuthentication(TokenAuthentication):
    """
    Wrapper for TokenAuthentication to allow custom token methods to authenticate users and allow access to API based
    on it
    """

    keyword = "Bearer"

    def authenticate(self, request):
        """
        overrides the `authenticate` function of Parent Class and returns the respected user or None if the user is not
        authenticated
        :param request: Django `request` object
        :return: Account Object or None
        """

        auth = request.META.get('HTTP_AUTHORIZATION').split()

        if not auth or auth[0].casefold() != self.keyword.casefold().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            token = TokenManager.objects.select_related('user').get(token=auth[1])
        except Exception:
            raise AuthenticationFailed('Unauthorized')

        if not token.user.is_active:
            raise AuthenticationFailed('Account Suspended!')

        if token.valid_upto < dt.now(tz=ZoneInfo('Asia/Kolkata')):
            token.delete()
            raise AuthenticationFailed('Token Expired!')
        return token.user, token
