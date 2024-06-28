from django.db import models


class Banner(models.Model):
    image = models.ImageField(upload_to="banner/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
