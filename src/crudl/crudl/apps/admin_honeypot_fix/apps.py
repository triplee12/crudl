from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminHoneypotFixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_honeypot'
    verbose_name = _("Admin Honeypot")

    def ready(self):
        from .admin import FixedLoginAttemptAdmin
