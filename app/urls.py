from django.urls import path

# from app.views import home, ArticleCreateView
from app.views import (
    ArticleListView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleCreateView,
)

urlpatterns = [
    # path("", home, name="home"),
    # path("articles/create/", create_article, name="create_article")
    path("create/", ArticleCreateView.as_view(), name="create_article"),
    path("", ArticleListView.as_view(), name="home"),
    path("<int:pk>/update/", ArticleUpdateView.as_view(), name="update_article"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="delete_article"),
]
