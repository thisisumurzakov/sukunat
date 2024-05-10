from django.contrib import admin

from .models import User, FCMToken

admin.site.register(User)
admin.site.register(FCMToken)
