from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    response = models.TextField()
