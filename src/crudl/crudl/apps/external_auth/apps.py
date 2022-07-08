from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExternalAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crudl.apps.external_auth'
    verbose_name: str = _('External Authentication')
