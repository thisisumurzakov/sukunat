from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Banner
from .serializers import BannerSerializer


class ActiveBannerView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]  # Adjust the permissions as necessary

    def get(self, request):
        active_banners = Banner.objects.filter(is_active=True).order_by("-created_at")
        serializer = BannerSerializer(
            active_banners, many=True, context={"request": request}
        )
        return Response(serializer.data)
