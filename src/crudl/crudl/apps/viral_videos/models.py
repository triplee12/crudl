import uuid
import re
from django.db import models
from django.utils.translation import gettext_lazy as _
from crudl.apps.core.models import CreationModificationDateBase, UrlBase


class ViralVideo(CreationModificationDateBase, UrlBase):
    uuid = models.UUIDField(primary_key=True, default=None, editable=False)
    title = models.CharField(_("Title"), max_length=255, blank=True)
    embed_code = models.TextField(_("Youtube embed code"), blank=True)
    anonymous_views = models.PositiveIntegerField(_("Anonymous impressions"), default=0)
    authenticated_views = models.PositiveIntegerField(_("Authenticated impressions"), default=0)

    class Meta:
        verbose_name = _("Viral video")
        verbose_name_plural = _("Viral videos")
    
    def __str__(self):
        return self.title
    
    def get_url_path(self):
        from django.urls import reverse
        return reverse("viral_videos:viral_video_detail",bkwargs={"pk":self.pk})
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.pk = uuid.uuid4()
        super().save(*args, **kwargs)

    def get_thumbnails(self):
        if not hasattr(self, '_thumbnail_url_cached'):
            self._thumbnail_url_cached = ""
            url_pattern = re.compile(r'src="https://wwww.youtube.com/embed/([^"]+)"')
            match = url_pattern.search(self.embed_code)
            if match:
                video_id = match.group()[0]
                self._thumbnail_url_cached = (f"https://www.youtube.com/vi/{video_id}/0.jpg")
        return self._thumbnail_url_cached

