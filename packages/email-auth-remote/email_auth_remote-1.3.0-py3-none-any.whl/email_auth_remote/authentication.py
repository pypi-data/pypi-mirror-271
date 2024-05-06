"""Модуль аутентификации с помощью auth endpoint."""

import logging
from rest_framework_simplejwt.authentication import AuthUser
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import Token
from dj_rest_auth.jwt_auth import JWTCookieAuthentication

logger = logging.getLogger(__name__)


class JWTStatelessCookieAuthentication(JWTCookieAuthentication):
    """
    An authentication plugin that hopefully authenticates requests through a JSON web
    token provided in a request cookie (and through the header as normal, with a
    preference to the header).
    """

    def get_user(self, validated_token: Token) -> AuthUser:
        """
        Returns a stateless user object which is backed by the given validated
        token.
        """
        if jwt_settings.USER_ID_CLAIM not in validated_token:
            # The TokenUser class assumes tokens will have a recognizable user
            # identifier claim.
            raise InvalidToken(_("Token contained no recognizable user identification"))

        return jwt_settings.TOKEN_USER_CLASS(validated_token)
