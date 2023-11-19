# myapp/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields you need
    # For example:
    # bio = models.TextField(blank=True)

    # Add related_name to avoid clashes with auth.User model
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # Use the email field for authentication
    REQUIRED_FIELDS = []  # Remove 'email' from the REQUIRED_FIELDS list

    def __str__(self):
        return self.email  # You can customize this based on your preference
