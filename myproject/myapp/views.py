from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser  # Update import to use CustomUser
import json

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            user = CustomUser.objects.create(username=username, email=email, password=password)  # Use CustomUser

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        print('email', email, 'password', password)

        # Authenticate using the email field
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            token, created = Token.objects.get_or_create(user=user)

            return Response({'status': 'success', 'token': token.key})
        else:
            return Response({'status': 'error', 'message': 'Invalid login credentials'})
