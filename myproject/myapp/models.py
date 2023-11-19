from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone



class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='myapp_auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
