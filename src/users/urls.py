from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SendCodeView, VerifyCodeView, UserView, LogoutView

urlpatterns = [
    path("send_code/", SendCodeView.as_view(), name="send_code"),
    path("verify_code/", VerifyCodeView.as_view(), name="send_code"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/", UserView.as_view(), name="user"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
