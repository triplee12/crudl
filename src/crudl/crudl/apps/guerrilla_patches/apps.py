from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GuerrillaPatchesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crudl.apps.guerrilla_patches'
    verbose_name: str = _("Guerrilla Patche")
