from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Tag


User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class AuthorSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "profile_photo"]

    def get_profile_photo(self, obj):
        return (
            obj.profile.profile_photo.url
            if hasattr(obj, "profile") and obj.profile.profile_photo
            else None
        )


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    is_author = serializers.SerializerMethodField()
    user = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "image",
            "text",
            "tags",
            "views",
            "user",
            "created_at",
            "updated_at",
            "is_author",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "views": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            post.tags.add(tag)
        return post

    def get_is_author(self, obj):
        request = self.context.get("request")
        return obj.user == request.user if request and request.user else False


class PostDetailSerializer(PostSerializer):
    replies = serializers.SerializerMethodField()

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ["replies"]

    def get_replies(self, obj):
        replies = obj.replies.filter()
        return PostSerializer(
            replies, many=True, context={"request": self.context.get("request")}
        ).data


class UserRepliesSerializer(PostSerializer):
    parent = PostSerializer()

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ["parent"]


class ReplyCreateSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ["parent"]
