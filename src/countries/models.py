from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=10)
    phone_code = models.CharField(max_length=10)
    flag = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.code + " " + self.name
