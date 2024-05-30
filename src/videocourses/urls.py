from django.urls import path
from .views import VideoCourseList, VideoList

urlpatterns = [
    path("list/", VideoCourseList.as_view(), name="videocourse-list"),
    path("videos/<int:video_course_id>/", VideoList.as_view(), name="video-list"),
]
