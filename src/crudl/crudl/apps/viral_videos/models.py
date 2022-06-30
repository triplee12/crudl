import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from crudl.apps.core.models import CreationModificationDateBase, UrlBase


class ViralVideo(CreationModificationDateBase, UrlBase):
    embed_code = models.TextField(_("Youtube embed code"), blank=True)

    def get_thumbnails(self):
        if not hasattr(self, '_thumbnail_url_cached'):
            self._thumbnail_url_cached = ""
            url_pattern = re.compile(r'src="https://wwww.youtube.com/embed/([^"]+)"')
            match = url_pattern.search(self.embed_code)
            if match:
                video_id = match.group()[0]
                self._thumbnail_url_cached = (f"https://www.youtube.com/vi/{video_id}/0.jpg")
        return self._thumbnail_url_cached

