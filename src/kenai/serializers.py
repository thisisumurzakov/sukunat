from rest_framework import serializers


class KenaiMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
