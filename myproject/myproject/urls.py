
# myproject/urls.py
from django.urls import path
from myapp.views import signup, user_login
from myapp.views import PostListCreateView, PostDeleteView, PostUpdateView
from django.urls import include, path

urlpatterns = [
path('signup/', signup, name='signup'),
path('login/', user_login, name='user_login'),
path('posts/<int:post_id>/', PostUpdateView.as_view(), name='post-update'),
path('post/<int:pk>/', PostDeleteView.as_view(), name='post-detail'),
path('posts/', PostListCreateView.as_view(), name='post-list-create'),
]










