from django.urls import path
from .views import CategoryListView, ArticleListView, ArticleDetailView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="article-category-list"),
    path("category/<int:category_id>/", ArticleListView.as_view(), name="article-list"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
]
