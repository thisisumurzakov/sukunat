from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    icon = models.FileField(upload_to="articles/category/", blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} {self.name}"


class Article(models.Model):
    image = models.ImageField(upload_to="articles/article/", blank=True, null=True)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    read_time = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="articles"
    )
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.title}"

    def save(self, *args, **kwargs):
        self.read_time = self.calculate_read_time(self.description)
        super().save(*args, **kwargs)

    def calculate_read_time(text):
        words_per_minute = 200
        words = text.split()
        num_words = len(words)
        read_time_minutes = round(num_words / words_per_minute)
        return read_time_minutes

    class Meta:
        ordering = ["-created_at"]
