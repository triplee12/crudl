from cProfile import label
from calendar import c
import re
import logging
from django.conf import settings
from django.db import models
from django.utils.timezone import now, timedelta
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import ListView
from .models import ViralVideo

POPULAR_FROM = getattr(settings, "VIRAL_VIDEOS_POPULAR_FROM", 500)

logger = logging.getLogger(__name__)


class ViralVideoList(ListView):
    template_name: str = "viral_videos/viral_video_list.html"
    model = ViralVideo

@vary_on_cookie
@cache_page(60)
def viral_video_detail(request, pk):
    yesterday = now() - timedelta(days=1)
    qs = ViralVideo.objects.annotate(
        total_views = models.F("authenticated_views") + models.F("anonymous_views"),
        label = models.Case(
            models.When(total_views__get=POPULAR_FROM, then=models.Value("popular")),
            models.When(created__gt=yesterday, then=models.Value("new")),
            default=models.Value("cool"),
            output_field=models.CharField(),
        ),
    )
    # DEBUG: check the SQL query that Django ORM generates
    logger.debug(f"Query: {qs.query}")
    qs = qs.filter(pk=pk)
    if request.user.is_authenticated:
        qs.update(authentiated_views = models.F("authenticated_views") + 1)
    else:
        qs.update(anonymous_views = models.F("anonymous_views") + 1)
    video = get_object_or_404(qs)
    return render(request, 'viral_videos/viral_video_detail.html', {'video': video})
