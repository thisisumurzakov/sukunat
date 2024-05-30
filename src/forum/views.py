from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from config.permissions import IsOwnerOrAuthenticated

from .models import Post
from .serializers import PostSerializer, PostDetailSerializer


class PostListView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(parent__isnull=True).prefetch_related("tags")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.prefetch_related("replies", "replies__user", "tags")
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
