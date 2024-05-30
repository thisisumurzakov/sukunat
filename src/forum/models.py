from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    image = models.ImageField(upload_to="forum/posts/", null=True, blank=True)
    text = models.TextField()
    # status = models.CharField(max_length=10,
    #                           choices=(('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')),
    #                           default='draft')
    tags = models.ManyToManyField("Tag", related_name="posts", null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def like_count(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "post")


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
