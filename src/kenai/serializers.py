from rest_framework import serializers


class AIChatSerializer(serializers.Serializer):
    message = serializers.CharField()
