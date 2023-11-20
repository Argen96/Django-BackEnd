from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

def get_user_id_from_token(token):
    user_model = get_user_model()
    try:
        user_id = AccessToken(token).get('user_id')
        return user_model.objects.get(pk=user_id)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error extracting user ID from token: {e}")
        return None