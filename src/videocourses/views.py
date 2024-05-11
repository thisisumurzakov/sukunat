from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from config.pagination import StandardResultsPagination

from .models import VideoCourse, Video
from .serializers import VideoCourseSerializer, VideoSerializer


class VideoCourseList(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    serializer_class = VideoCourseSerializer

    def get_queryset(self):
        return VideoCourse.objects.filter(is_active=True)


class VideoList(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    serializer_class = VideoSerializer

    def get_queryset(self):
        """
        This view should return a list of all the videos
        for the video course as determined by the video_course_id portion of the URL.
        """
        video_course_id = self.kwargs['video_course_id']
        return Video.objects.filter(video_course_id=video_course_id)
