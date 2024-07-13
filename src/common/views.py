from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Banner
from .serializers import BannerSerializer, KenaiMessageSerializer


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
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=KenaiMessageSerializer)
    def post(self, request):
        serializer = KenaiMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            data={
                "response": f"Erkin make a payment to openai!\n{request.user.get_full_name()}'s message was: {serializer.validated_data['message']}"
            }
        )
