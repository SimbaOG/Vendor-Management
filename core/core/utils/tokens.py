import secrets
import string

from django.conf import settings


def generate_auth_token():
    """Generate a cryptographically secure authentication token."""
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(settings.AUTH_TOKEN_LENGTH))
    return token
