from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LikesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crudl.apps.likes'
    verbose_name = _("Like")

