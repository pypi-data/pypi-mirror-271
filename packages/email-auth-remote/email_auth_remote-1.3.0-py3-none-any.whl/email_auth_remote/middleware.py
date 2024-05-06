from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    AuthenticationFailed,
)

from .authentication import JWTStatelessCookieAuthentication


class JWTStatelessCookieAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authentication = JWTStatelessCookieAuthentication()

        try:
            result = authentication.authenticate(request)
            if result is not None:
                request.user = result[0]
        except (InvalidToken, AuthenticationFailed):
            pass

        return self.get_response(request)
