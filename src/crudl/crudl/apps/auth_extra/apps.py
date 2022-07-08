from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthExtraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crudl.apps.auth_extra'
    verbose_name: str = _('Auth extra config')
