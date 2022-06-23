from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crudl.apps.accounts'
    verbose_name = _("Accounts")
    
    def ready(self):
        pass


class SocialDjangoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_django'
    verbose_name = _("Social Authentication")
