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


class KenaiAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        user_message = request.data.get("message")
        if not user_message:
            return Response(status=400)
        return Response(data={"response": "Erkin make a payment to openai!"})
