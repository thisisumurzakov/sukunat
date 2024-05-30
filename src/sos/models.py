from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    phone_number = PhoneNumberField(_("phone number"))
    name = models.CharField(max_length=150)
