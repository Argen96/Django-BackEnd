# myapp/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import timedelta 
from django.contrib.auth.hashers import check_password
from .models import CustomUser  
import json

@csrf_exempt
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Hash the password using make_password
            hashed_password = make_password(password)
            
            user = CustomUser(username=username, email=email, password=hashed_password)
            user.save()

            return JsonResponse({'status': 'success', 'message': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



from traceback import print_exc

from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = authenticate(request, email=email, password=password)

            if user is not None and check_password(password, user.password):
                login(request, user)

                # Generate a refresh token
                refresh = RefreshToken.for_user(user)

                # Set the expiration time for the access token (adjust as needed)
                access_token = refresh.access_token
                access_token.set_exp(lifetime=timedelta(hours=1))  # Set expiration time (adjust as needed)

                # Include user_id in the token
                token_payload = {
                    'token': str(access_token),
                    'user_id': user.id,
                }

                return Response({'status': 'success', 'data': token_payload})
            else:
                return Response({'status': 'error', 'message': 'Invalid login credentials'})
        except Exception as e:
            print_exc()  # Print the traceback
            return Response({'status': 'error', 'message': 'An error occurred during login'})
    else:
        return Response({'status': 'error', 'message': 'Invalid request method'})
