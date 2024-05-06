from django.contrib import admin
from django.contrib.auth.models import User, Group
from .settings import api_settings

if api_settings.ADMIN_USER_UNREGISTER:
    admin.site.unregister(User)
    admin.site.unregister(Group)
