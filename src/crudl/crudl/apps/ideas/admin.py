from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from crudl.apps.core.admin import get_multilingual_field_names, LanguageChoicesForm

from .models import Idea, IdeaTranslations

class IdeaTranslationsForm(LanguageChoicesForm):
    class Meta:
        model = IdeaTranslations
        fields = "__all__"


class IdeaTranslationsInline(admin.StackedInline):
    form = IdeaTranslationsForm
    model = IdeaTranslations
    extra = 0


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    inlines = [IdeaTranslationsInline]
    fieldsets = [
        (_("Title and Content"), {
            # "fields": get_multilingual_field_names("title") + get_multilingual_field_names("content")
            "fields": ["title", "content", "author", "categories", "picture",]
        }),
    ]