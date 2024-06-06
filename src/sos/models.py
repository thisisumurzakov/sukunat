from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    phone_number = PhoneNumberField(_("phone number"))
    name = models.CharField(max_length=150)


class TrackingSession(models.Model):
    track_id = models.CharField(max_length=36, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
