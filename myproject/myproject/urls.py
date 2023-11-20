
# myproject/urls.py
from django.urls import path
from myapp.views import signup, user_login
from myapp.views import PostListCreateView, CommentListCreateView, PostDetailView
from django.urls import include, path

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='user_login'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
]










