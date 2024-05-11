from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contact
from .serializers import ContactSerializer
from .tasks import send_distress_signal


class ContactCreateGetUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        if Contact.objects.filter(user=request.user).exists():
            return Response({"message": "You have already added a contact"}, status=400)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = request.user
        serializer.save()
        return Response(serializer.data, status=201)

    def get(self, request):
        try:
            contact = Contact.objects.get(user=request.user)
            return Response(self.get_serializer(contact).data, status=200)
        except Contact.DoesNotExist:
            return Response({'message': 'Contact not found'}, status=404)

    def put(self, request, *args, **kwargs):
        try:
            contact = Contact.objects.get(user=request.user)
        except Contact.DoesNotExist:
            return Response({'message': 'Contact not found'}, status=404)

        serializer = self.get_serializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class SendDistressSignalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            contact = Contact.objects.get(user=request.user)
            send_distress_signal.delay(contact.id)
            return Response({"message": "Distress signal is being processed."})
        except Contact.DoesNotExist:
            return Response({'message': 'Contact not found'}, status=404)
