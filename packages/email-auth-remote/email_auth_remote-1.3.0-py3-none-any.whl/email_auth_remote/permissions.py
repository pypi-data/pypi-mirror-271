"""Модуль разрешений приложения email_auth."""
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView


class IsDesigner(BasePermission):
    """Разрешение уровня представления для дизайнера."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_designer  # type: ignore[union-attr]


class IsSeller(BasePermission):
    """Разрешение уровня представления для продавца."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_seller  # type: ignore[union-attr]


class IsDesignerOrReadOnly(IsDesigner):
    """Разрешение для дизайнера, либо ReadOnly для методов в SAFE_METHODS."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return super().has_permission(request, view)


class IsSellerOrReadOnly(IsSeller):
    """Разрешение для продавца, либо ReadOnly для методов в SAFE_METHODS."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return super().has_permission(request, view)
