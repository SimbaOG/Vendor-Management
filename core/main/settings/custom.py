"""
Settings specific to this application (No Django or 3rd Party Settings)
"""

IN_DOCKER = True

AUTH_TOKEN_LENGTH = 32

TOKEN_MAX_EXPIRY = 172800  # Tokens last for 2 days

API_PREFIX = 'api'
