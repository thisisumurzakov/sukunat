from django.urls import path
from .views import PostListView, PostDetailView, ReplyCreateView

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path(
        "posts/<int:post_id>/replies/", ReplyCreateView.as_view(), name="reply-create"
    ),
]
