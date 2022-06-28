from django.urls import path

from .views import (
    # IdeaList,
    # idea_list,
    IdeaListView,
    IdeaDetail,
    add_or_change_idea,
    delete_idea,
    idea_handout_pdf,
    download_idea_picture
)

urlpatterns = [
    path("", IdeaListView.as_view(), name="idea_list"),
    path("add/", add_or_change_idea, name="add_idea"),
    path("<uuid:pk>/", IdeaDetail.as_view(), name="idea_detail"),
    path("<uuid:pk>/change/", add_or_change_idea, name="change_idea"),
    path("<uuid:pk>/delete/", delete_idea, name="delete_idea"),
    path("<uuid:pk>/handout/", idea_handout_pdf, name="idea_handout"),
    path("<uuid:pk>/download-picture/", download_idea_picture, name="download_idea_picture"),
]