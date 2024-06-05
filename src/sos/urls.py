from django.urls import path
from .views import ContactCreateGetUpdateView, SendDistressSignalView, live_tracking

urlpatterns = [
    path("contacts/", ContactCreateGetUpdateView.as_view(), name="contact-create-get"),
    path("send-distress/", SendDistressSignalView.as_view(), name="send-distress"),
    path("track/<uuid:tracking_id>/", live_tracking, name="live_tracking"),
    # path('contacts/<int:pk>/', ContactCreateGetUpdateView.as_view(), name='contact-update'),
]
