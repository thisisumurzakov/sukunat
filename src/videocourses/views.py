from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from config.pagination import StandardResultsPagination
from rest_framework.response import Response

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
        video_course_id = self.kwargs["video_course_id"]
        return Video.objects.filter(video_course_id=video_course_id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            video_course = VideoCourse.objects.get(id=self.kwargs["video_course_id"])
            video_course_serializer = VideoCourseSerializer(
                video_course, context={"request": request}
            )

            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.data["video_course"] = video_course_serializer.data
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        video_course = VideoCourse.objects.get(id=self.kwargs["video_course_id"])
        video_course_serializer = VideoCourseSerializer(video_course)
        return Response(
            {"video_course": video_course_serializer.data, "results": serializer.data}
        )
