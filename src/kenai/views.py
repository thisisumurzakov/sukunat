from drf_yasg.utils import swagger_auto_schema
from groq import Groq
from openai import OpenAI
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation
from django.conf import settings
import openai

from .serializers import AIChatSerializer


class ChatAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=AIChatSerializer)
    def post(self, request, *args, **kwargs):
        user_message = request.data.get("message")
        user = request.user  # This assumes you are using Django's authentication system

        if not user_message:
            return Response(
                {"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Configure the prompt for the ChatGPT model
        try:
            client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
            )
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=[
                    {
                        "role": "system",
                        "content": "Your name is Kenai. You are a psychologist helping women.",
                    },
                    {"role": "user", "content": user_message},
                ],
            )

            # Save the conversation
            conversation = Conversation.objects.create(
                user=user,
                message=user_message,
                response=response.choices[0].message[
                    "content"
                ],  # Accessing the response content
            )

            return Response(
                {"response": conversation.response}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GroqAPIVIEW(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=AIChatSerializer)
    def post(self, request, *args, **kwargs):
        s = AIChatSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user_message = s.validated_data.get("message")
        user = request.user  # This assumes you are using Django's authentication system

        if not user_message:
            return Response(
                {"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            client = Groq(
                api_key="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",
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Your name is Kenai. You are a psychologist helping women.",
                    },
                    {"role": "user", "content": user_message},
                ],
                model="llama3-8b-8192",
            )

            return Response(
                {"response": chat_completion.choices[0].message.content},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
