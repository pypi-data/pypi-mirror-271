from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck


def enforce_csrf(request):
    """
    Enforce CSRF validation for session based authentication.
    """

    def dummy_get_response(request):  # pragma: no cover
        return None

    check = CSRFCheck(dummy_get_response)
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        # CSRF failed, bail with explicit error message
        raise exceptions.PermissionDenied(f"CSRF Failed: {reason}")
