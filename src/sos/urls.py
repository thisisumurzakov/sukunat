from django.urls import path
from .views import ContactCreateGetUpdateView

urlpatterns = [
    path('contacts/', ContactCreateGetUpdateView.as_view(), name='contact-create-get'),
    #path('contacts/<int:pk>/', ContactCreateGetUpdateView.as_view(), name='contact-update'),
]
