from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crudl.apps.music'
    verbose_name = _('Music')
