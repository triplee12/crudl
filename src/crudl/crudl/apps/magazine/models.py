# from audioop import reverse
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from crudl.apps.core.models import MetaTagsBase, CreationModificationDateBase, UrlBase

class NewsArticle(models.Model):
    title = models.CharField(_("Title"), max_length=200, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(_("Content"))
    theme = models.CharField(_("Theme"), max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(_("Created at"), auto_created=True, auto_now=True)

    class Meta:
        verbose_name = _("News Article")
        verbose_name_plural = _("News Articles")

    def __str__(self):
        return  self.title


class Idea(MetaTagsBase, CreationModificationDateBase, UrlBase):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("Slug for URLs"), max_length=250)
    content = models.TextField(_("content"),)
    
    class Meta:
        verbose_name = _("Idea")
        verbose_name_plural = _("Ideas")
    
    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse("idea_details", kwargs={
    #         "idea_id": str(self.pk),
    #     })
    
    def get_url_path(self):
        return reverse("idea_details", kwargs={
            "idea_id": str(self.pk),
            "slug": self.slug,
        })
