# myapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Attempt to create a User object
            user = User.objects.create(username=username, email=email, password=password)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            # Return a detailed error message
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
