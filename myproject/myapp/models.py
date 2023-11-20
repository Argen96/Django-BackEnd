# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .utils import get_user_id_from_token

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='myapp_auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = 'myapp.serializers.PostSerializer'  # Corrected import
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        from .serializers import PostSerializer
        # Associate the post with the current user
        serializer.save(author=self.request.user)

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = 'myapp.serializers.CommentSerializer'  # Corrected import
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        from .serializers import CommentSerializer
        # Associate the comment with the current user and post
        serializer.save(author=self.request.user, post_id=self.kwargs['post_id'])
