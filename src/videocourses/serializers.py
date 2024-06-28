from rest_framework import serializers


class VideoCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()
    title = serializers.CharField()
    description = serializers.CharField()
    video_count = serializers.IntegerField(read_only=True)
    total_duration = serializers.DurationField(read_only=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    # class Meta:
    #     model = VideoCourse
    #     fields = ['id', 'image', 'title', 'description', 'video_count', 'total_duration', 'created_at', 'updated_at']


class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()
    title = serializers.CharField()
    description = serializers.CharField()
    youtube_url = serializers.URLField()
    youtube_id = serializers.CharField()
    duration = serializers.DurationField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    # class Meta:
    #     model = Video
    #     fields = ['id', 'title', 'youtube_url', 'duration', 'created_at', 'updated_at', 'video_course']
