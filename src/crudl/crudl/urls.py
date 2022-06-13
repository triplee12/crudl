from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from crudl.apps.core import views as core_views

urlpatterns = i18n_patterns(
    path("", lambda request: redirect("ideas:idea_list")),
    # path("", lambda request: redirect("locations:location_list")),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ideas/", include(("crudl.apps.ideas.urls", "ideas"), namespace="ideas")),
    path("locations/", include(("crudl.apps.locations.urls", "locations"), namespace="locations")),
    path("search/", include("haystack.urls")),
    path("js_settings/", core_views.js_settings, name="js_settings"),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)