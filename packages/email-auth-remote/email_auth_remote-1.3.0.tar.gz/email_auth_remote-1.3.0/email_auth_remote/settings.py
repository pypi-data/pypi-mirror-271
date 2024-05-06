from django.conf import settings
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, "EMAIL_AUTH_REMOTE", None)

DEFAULTS = {
    "JWT_REFRESH_URL": None,
    "JWT_ACCESS_CHECK_URL": None,
    "ADMIN_LOGIN_URL": None,
    "LOGOUT_URL": None,
    "ADMIN_USER_UNREGISTER": True,
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = ()

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
