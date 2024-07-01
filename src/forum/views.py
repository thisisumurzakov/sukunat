from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from config.permissions import IsOwnerOrAuthenticated
from config.pagination import StandardCursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer, PostDetailSerializer


class PostListView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardCursorPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "type",
                openapi.IN_QUERY,
                description="Filter posts by type: 'user_posts', 'user_replies', or 'all'. Default is 'all'.",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        content_type = self.request.query_params.get("type", "all")

        if content_type == "user_posts":
            return Post.objects.filter(user=user, parent__isnull=True).prefetch_related(
                "tags"
            )
        elif content_type == "user_replies":
            return (
                Post.objects.filter(user=user, parent__isnotnull=True)
                .select_related("parent")
                .prefetch_related("tags")
            )
        elif content_type == "all":
            return Post.objects.filter(parent__isnull=True).prefetch_related("tags")
        else:
            return Post.objects.none()  # Safely handle unexpected values

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.prefetch_related("replies", "replies__user", "tags")
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ReplyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            parent_post = Post.objects.get(id=post_id, parent__isnull=True)
        except Post.DoesNotExist:
            return Response({"error": "Parent post not found"}, status=404)

        data = request.data.copy()
        data["parent"] = parent_post.id
        serializer = PostSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
