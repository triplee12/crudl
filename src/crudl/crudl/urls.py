from nis import cat
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.sitemaps import views as sitemaps_views
from django.contrib.sitemaps import GenericSitemap
import debug_toolbar
from crudl.apps.core import views as core_views
from crudl.apps.external_auth.views import (index, dashboard, logout)
from crudl.apps.category import views as category_views
from crudl.apps.music.models import Song
from crudl.apps.music.views import RESTSongList, RESTSongDetail


class CrudlSitemap(GenericSitemap):
    limit = 50

    def location(self, obj):
        return obj.get_url_path()

song_info_dict = {
    "queryset": Song.objects.all(),
    "date_field": "modified",
}
sitemaps = {"music": CrudlSitemap(song_info_dict, priority=1.0)}

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("rest-api/songs/", RESTSongList.as_view(), name="rest_song_list"),
    path("rest-api/songs/<uuid:pk>/", RESTSongDetail.as_view(), name="rest_song_detail"),
    path("sitemap.xml", sitemaps_views.index, {"sitemaps": sitemaps}),
    path("sitemap-<str:section>.xml", sitemaps_views.sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

urlpatterns += i18n_patterns(
    path("", index, name="index"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout, name="logout"),
    path("", include("social_django.urls")),
    path("", lambda request: redirect("ideas:idea_list")),
    # path("", lambda request: redirect("locations:location_list")),
    #path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ideas/", include(("crudl.apps.ideas.urls", "ideas"), namespace="ideas")),
    path("news/", include(("crudl.apps.news.urls", "news"), namespace="news")),
    path("locations/", include(("crudl.apps.locations.urls", "locations"), namespace="locations")),
    path("search/", include("haystack.urls")),
    path("js_settings/", core_views.js_settings, name="js_settings"),
    path("upload-file/", core_views.upload_file, name="upload_file"),
    path("likes/", include(("crudl.apps.likes.urls", "likes"), namespace="likes")),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("management/", admin.site.urls),
    path("idea-categories/", category_views.IdeaCategoryListView.as_view(), name="idea_categories",),
    path("songs/", include("crudl.apps.music.urls", namespace="music")),
    path("viral-videos/", include("crudl.apps.viral_videos.urls", namespace="viral_videos")),
)
urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)