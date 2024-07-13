from django.urls import path
from .views import OpenaiAPIView

urlpatterns = [
    path("chat/", OpenaiAPIView.as_view(), name="kenai-openai-chat"),
]
