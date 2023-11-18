
# myproject/urls.py
from django.urls import path
from myapp.views import signup

urlpatterns = [
    path('signup/', signup, name='signup'),
]
