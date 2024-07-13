import time

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from openai import OpenAI, APIConnectionError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation
from .serializers import KenaiMessageSerializer


class OpenaiAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=KenaiMessageSerializer)
    def post(self, request, *args, **kwargs):
        serializer = KenaiMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_message = serializer.validated_data.get("message")
        user = request.user  # Assumes Django's authentication system

        if not user_message:
            return Response({"error": "Message is required"}, status=400)

        # Retrieve the last 5 conversation pairs (message and response) for context
        last_conversations = Conversation.objects.filter(user=user).order_by("-id")[:5]
        past_messages = []
        for conv in reversed(last_conversations):
            past_messages.append({"role": "user", "content": conv.message})
            past_messages.append({"role": "assistant", "content": conv.response})

        # Configure the prompt for the ChatGPT model
        try:
            response = self.make_openai_request(
                {
                    "model": "gpt-4-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Your name is Kenai. You are a psychologist helping women. You do not answer to unrelated questions",
                        },
                        *past_messages,  # Spread past_messages directly into the array
                        {"role": "user", "content": user_message},
                    ],
                }
            )

            # Save the conversation
            Conversation.objects.create(
                user=user,
                message=user_message,
                response=response.choices[0].message.content.strip(),
            )

            return Response(
                {"response": response.choices[0].message.content.strip()}, status=200
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def make_openai_request(self, data):
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        retries = 3
        for attempt in range(retries):
            try:
                response = client.chat.completions.create(**data)
                return response
            except APIConnectionError:
                if attempt < retries - 1:  # if it's not the last attempt
                    time.sleep(2**attempt)  # exponential back-off
                    continue
                else:
                    raise  # re-raise the last exception
