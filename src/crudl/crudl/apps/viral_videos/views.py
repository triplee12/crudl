from calendar import c
import re
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .models import ViralVideo

@vary_on_cookie
@cache_page(60)
def viral_video_detail(request, pk):
    video = get_object_or_404(ViralVideo, pk=pk)
    return render(request, 'viral_videos/viral_video_detail.html', {'video': video})
