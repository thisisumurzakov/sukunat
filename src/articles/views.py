from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from config.pagination import StandardResultsPagination

from .models import Category, Article
from .serailizers import (
    CategorySerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
)


class CategoryListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True)

    def get_serializer_context(self):
        """
        Overriding get_serializer_context to add request to the context.
        """
        context = super(CategoryListView, self).get_serializer_context()
        return context


class ArticleListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        """
        This view should return a list of all the videos
        for the video course as determined by the video_course_id portion of the URL.
        """
        video_course_id = self.kwargs["category_id"]
        return Article.objects.filter(category_id=video_course_id).defer("description")


class ArticleDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
