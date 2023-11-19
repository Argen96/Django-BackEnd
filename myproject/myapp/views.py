# myapp/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse
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

# myapp/views.py
from django.http import Http404

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            # Authenticate using both email and password
            user = authenticate(request, email=email, password=password)

            if user is not None and check_password(password, user.password):
                login(request, user)

                # Get existing token or create a new one
                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)

                return Response({'status': 'success', 'token': token.key, 'user_id': user.id})
            else:
                return Response({'status': 'error', 'message': 'Invalid login credentials'})
        except Exception as e:
            print_exc()  # Print the traceback
            return Response({'status': 'error', 'message': 'An error occurred during login'})
    else:
        return Response({'status': 'error', 'message': 'Invalid request method'})


