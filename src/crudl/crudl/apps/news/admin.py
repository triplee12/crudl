from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Article

admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (_("Title and Content"), {"fields": ["title", "slug", "content"]}),
        (_("Publish_status"), {"fields": ["publishing_status"]}),
    ]
