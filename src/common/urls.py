from django.urls import path
from .views import ActiveBannerView

urlpatterns = [
    path("banners/", ActiveBannerView.as_view(), name="active-banners"),
]
