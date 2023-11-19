
# myproject/urls.py


from django.urls import path
from myapp.views import signup, user_login

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='user_login'),
]