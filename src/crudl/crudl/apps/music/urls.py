from django.urls import path
from .views import SongListView, SongDetailView

app_name = "music"

urlpatterns = [
    path("", SongListView.as_view(), name="song_list"),
    path("<uuid:pk>/", SongDetailView.as_view(), name="song_detail"),
]
