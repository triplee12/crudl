from django.url import path
from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path("article/", ArticleListView.as_view(), name="article_list"),
    path("<uuid:pk>/", ArticleDetailView.as_view(), name="article_detail"),
]