from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    icon = models.FileField(upload_to='articles/category/', blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} {self.name}'


class Article(models.Model):
    image = models.ImageField(upload_to='articles/article/', blank=True, null=True)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} {self.title}'

    class Meta:
        ordering = ['-created_at']
