from re import I
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# from django_mptt_admin.admin import DjangoMpttAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from crudl.apps.core.admin import LanguageChoicesForm
from .models import Category, CategoryTranslations

class CategoryTranslationsForm(LanguageChoicesForm):
    class Meta:
        model = CategoryTranslations
        fields = "__all__"


class CategoryTranslationsInline(admin.StackedInline):
    form = CategoryTranslationsForm
    model = CategoryTranslations
    extra = 0


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    inlines = [CategoryTranslationsInline]
    fieldsets = [
        (_("Title"), {
            "fields": ["title",]
        }),
    ]
    list_display = ["title", "created", "modified"]
    list_filter = ["created"]
