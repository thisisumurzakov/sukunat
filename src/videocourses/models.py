from django.db import models
from django.db.models import Sum


class VideoCourse(models.Model):
    image = models.ImageField(upload_to="videocourses/")
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    lang = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def video_count(self):
        return self.videos.count()

    @property
    def total_duration(self):
        total = self.videos.aggregate(sum_duration=Sum("duration"))
        return total["sum_duration"] or 0  # Returns 0 if there are no videos

    def __str__(self):
        return f"{self.id} {self.title}"

    class Meta:
        ordering = ["-created_at"]


class Video(models.Model):
    image = models.ImageField(upload_to="videos/", null=True, blank=True)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    video_course = models.ForeignKey(
        VideoCourse, on_delete=models.CASCADE, related_name="videos"
    )
    youtube_url = models.URLField(max_length=200)
    youtube_id = models.CharField(max_length=100, null=True, blank=True)
    duration = models.DurationField()  # Stores duration as timedelta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.video_course.save()  # Trigger update on VideoCourse

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.video_course.save()  # Update VideoCourse after deletion of a video

    def __str__(self):
        return f"{self.id} {self.title}"
