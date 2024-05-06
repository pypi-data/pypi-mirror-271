from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from .settings import api_settings


class AdminLoginView(View):
    redirect_field_name = REDIRECT_FIELD_NAME
    login_url = api_settings.ADMIN_LOGIN_URL

    def get(self, request):
        next_url = request.GET.get(self.redirect_field_name)
        if next_url:
            return HttpResponseRedirect(self.login_url + f"?next={next_url}")
        return HttpResponseRedirect(self.login_url)


class AdminLogoutView(LogoutView):

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        """
        Does absolutely nothing to log the user out.
        Not meant to be used.
        """
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            response = HttpResponseRedirect(redirect_to)
        else:
            response = super().get(request, *args, **kwargs)
        return response
