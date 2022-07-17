from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ViralVideosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crudl.apps.viral_videos'
    verbose_name: str = _('Viral videos')

    def ready(self):
        from .signals import inform_administrators
        from .checks import settings_check
