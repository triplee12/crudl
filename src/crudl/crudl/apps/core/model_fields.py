from django.conf import settings
from django.db import models
from django.utils.translation import  get_language
from django.utils import translation


class TranslatedField(object):
    def __init__(self, field_name):
        self.field_name = field_name
    
    def __get__(self, instance, owner):
        lang_code = translation.get_language()
        if lang_code == settings.LANGUAGE_CODE:
            # The fields of the default language are in the manin model
            return getattr(instance, self.field_name)
        else:
            # The fields of the orther languages are in the translation
            # Model, but falls back to the main model
            translations = instance.translations.filter(
                language = lang_code,
            ).first() or instance
            return getattr(translations, self.field_name)