from rest_framework import serializers


class BannerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()


class KenaiMessageSerializer(serializers.Serializer):
    message = serializers.CharField()
