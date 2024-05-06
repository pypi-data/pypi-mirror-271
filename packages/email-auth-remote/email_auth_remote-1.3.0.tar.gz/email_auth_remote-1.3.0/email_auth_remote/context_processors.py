from .settings import api_settings


def constants(request):
    return {
        "JWT_ACCESS_CHECK_URL": api_settings.JWT_ACCESS_CHECK_URL,
        "JWT_REFRESH_URL": api_settings.JWT_REFRESH_URL,
        "LOGOUT_URL": api_settings.LOGOUT_URL,
    }
