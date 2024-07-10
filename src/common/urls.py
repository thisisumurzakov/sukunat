from django.urls import path
from .views import ActiveBannerView, KenaiAPIView

urlpatterns = [
    path("banners/", ActiveBannerView.as_view(), name="active-banners"),
    path("kenai/", KenaiAPIView.as_view(), name="kenai"),

]
