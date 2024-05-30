import random
import redis
from django.conf import settings
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from config.utils import get_sms_client
from .models import User, FCMToken
from .serializers import (
    UserSerializer,
    VerifyCodeSerializer,
    SendCodeSerializer,
    LogutSerializer,
)

# Initialize Redis client
redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


class SendCodeView(APIView):
    """
    View to send a verification code to the user's phone number.
    """

    @swagger_auto_schema(request_body=SendCodeSerializer)
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = str(serializer.validated_data["phone_number"])
        code = random.randint(100000, 999999)
        message_code = f"Код для мобильного приложения Sukunat: {code}"
        code = "475985"  # should be removed
        sms_client = get_sms_client()  # Get the dynamically chosen SMS client
        success, message = sms_client.send_sms(phone_number, code)
        redis_client.set(phone_number, code, ex=300)
        return Response(status=200)


class VerifyCodeView(APIView):
    """
    View to verify the code sent to the user's phone number.
    """

    @swagger_auto_schema(
        request_body=VerifyCodeSerializer,
        responses={
            200: openapi.Response(
                description="Verify SMS Code",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            )
        },
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = str(serializer.validated_data["phone_number"])
        # Retrieve the code from Redis
        stored_code = redis_client.get(phone_number)
        if stored_code and stored_code == serializer.validated_data["code"]:
            with transaction.atomic():
                user, created = User.objects.get_or_create(phone_number=phone_number)
                if created:
                    user.set_unusable_password()
                    user.save()

                fcm_token = serializer.validated_data.get("fcm_token", None)
                if fcm_token:
                    FCMToken.objects.get_or_create(user=user, token=fcm_token)

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"message": "Invalid or expired code"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get User's Info",
        operation_description="Retrieves the authenticated user's info.",
        responses={
            200: UserSerializer,
        },
        tags=["User"],
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if user and user.is_active:
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "User not found or inactive"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: "Bad Request"},
        operation_description="Partially update the user's first name, last name, and email.",
        operation_summary="Update User Info",
        tags=["User"],
    )
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LogutSerializer)
    def post(self, request):
        try:
            serializer = LogutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Optionally, get the FCM token from the request
            fcm_token = serializer.validated_data.get("fcm_token", None)

            # If an FCM token is provided, remove it from the database
            if fcm_token:
                FCMToken.objects.filter(token=fcm_token, user=request.user).delete()

            # Decode and validate the refresh token
            token = RefreshToken(serializer.validated_data["refresh"])

            # Blacklist the refresh token to revoke its validity
            token.blacklist()

            return Response(
                {"message": "Successfully logged out."}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"message": "Failed to log out."}, status=status.HTTP_400_BAD_REQUEST
            )
