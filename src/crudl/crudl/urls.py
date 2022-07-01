from nis import cat
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from crudl.apps.core import views as core_views
from crudl.apps.external_auth.views import (index, dashboard, logout)
from crudl.apps.category import views as category_views

urlpatterns = i18n_patterns(
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
    path("likes/", include(("myproject.apps.likes.urls", "likes"), namespace="likes")),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("management/", admin.site.urls),
    path("idea-categories/", category_views.IdeaCategoryListView.as_view(), name="idea_categories",),

)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)