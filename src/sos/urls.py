from django.urls import path
from .views import ContactCreateGetUpdateView, SendDistressSignalView

urlpatterns = [
    path('contacts/', ContactCreateGetUpdateView.as_view(), name='contact-create-get'),
    path('send-distress/', SendDistressSignalView.as_view(), name='send-distress'),
    #path('contacts/<int:pk>/', ContactCreateGetUpdateView.as_view(), name='contact-update'),
]
