import uuid

from django.shortcuts import render
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contact, TrackingSession
from .serializers import ContactSerializer, DistressSignalSerializer
from .tasks import send_distress_signal


class ContactCreateGetUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        if Contact.objects.filter(user=request.user).exists():
            return Response({"message": "You have already added a contact"}, status=400)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["user"] = request.user
        serializer.save()
        return Response(serializer.data, status=201)

    def get(self, request):
        try:
            contact = Contact.objects.get(user=request.user)
            return Response(self.get_serializer(contact).data, status=200)
        except Contact.DoesNotExist:
            return Response({"message": "Contact not found"}, status=404)

    def put(self, request, *args, **kwargs):
        try:
            contact = Contact.objects.get(user=request.user)
        except Contact.DoesNotExist:
            return Response({"message": "Contact not found"}, status=404)

        serializer = self.get_serializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class SendDistressSignalView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=DistressSignalSerializer)
    def post(self, request):
        try:
            serializer = DistressSignalSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            latitude = serializer.validated_data["latitude"]
            longitude = serializer.validated_data["longitude"]
            if not latitude or not longitude:
                return Response(
                    {
                        "error": "Location coordinates (latitude and longitude) are required."
                    },
                    status=400,
                )

            contact = Contact.objects.get(user=request.user)

            tracking_id = uuid.uuid4()
            TrackingSession.objects.create(track_id=tracking_id, user=request.user)
            live_tracking_url = request.build_absolute_uri(
                reverse("live_tracking", args=[tracking_id])
            )

            contact = Contact.objects.get(user=request.user)
            send_distress_signal.delay(str(contact.phone_number), live_tracking_url)

            return Response(
                {
                    "message": "Distress signal is being processed.",
                    "tracking_url": live_tracking_url,
                }
            )
            # send_distress_signal.delay(str(contact.phone_number), latitude, longitude)
            # return Response({"message": "Distress signal is being processed."})
        except Contact.DoesNotExist:
            return Response({"message": "Contact not found"}, status=404)


def live_tracking(request, tracking_id):
    return render(request, "sos/live_tracking.html", {"tracking_id": tracking_id})
