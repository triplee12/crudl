from doctest import debug_script
from enum import unique
import os
from pydoc import describe
from tabnanny import verbose
import uuid
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.text import slugify
from crudl.apps.core.models import CreationModificationDateBase, UrlBase

def upload_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    artist = slugify(instance.artist)
    title = slugify(instance.title)
    return f"music/{artist}--{title}{filename_ext.lower()}"


class Song(CreationModificationDateBase, UrlBase):
    uuid = models.UUIDField(primary_key=True, default=None, editable=False)
    artist = models.CharField(_("Artist"), max_length=250)
    title = models.CharField(_("Title"), max_length=250)
    description = models.TextField(_("Description"))
    url = models.URLField(_("URL"), blank=True)
    image = models.ImageField(_("Image"), upload_to=upload_to, blank=True, null=True)

    class Meta:
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")
        unique_together = ["artist", "title"]
    
    def __str__(self):
        return f"{self.artist} - {self.title}"
    
    def get_url_path(self):
        return reverse("music:song_detail", kwargs={"pk":self.pk})
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.pk = uuid.uuid4()
        super().save(*args, **kwargs)
