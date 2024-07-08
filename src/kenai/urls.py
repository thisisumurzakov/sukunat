from django.urls import path
from .views import ChatAPIView, GroqAPIVIEW

urlpatterns = [
    path("chat/", GroqAPIVIEW.as_view(), name="chat_api"),
]
