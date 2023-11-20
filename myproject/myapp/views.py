# myapp/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import timedelta 
from traceback import print_exc
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Post, Comment
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer, CommentSerializer
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
                access_token.set_exp(lifetime=timedelta(hours=10))  # Set expiration time (adjust as needed)

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

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Access the token from the request
        token = self.request.auth

        # Use the token as needed (e.g., extract user_id)
        user_id = token.payload.get('user_id')

        # Filter the queryset to get only the posts associated with the current user
        queryset = Post.objects.filter(author_id=user_id)
        return queryset

    def perform_create(self, serializer):
        # Access the token from the request
        token = self.request.auth

        # Use the token as needed (e.g., extract user_id)
        user_id = token.payload.get('user_id')

        # Set the author field directly in the serializer
        serializer.validated_data['author_id'] = user_id  # Assuming 'author_id' is the correct field in your serializer
        serializer.save()

        return Response({'status': 'success', 'message': 'Post created successfully'}, status=status.HTTP_201_CREATED)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the user making the request is the owner of the post
        if request.user != instance.author:
            return Response({'status': 'error', 'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({'status': 'success', 'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Access the token from the request
        token = self.request.auth

        # Use the token as needed (e.g., extract user_id)
        user_id = token.payload.get('user_id')

        # Set the author field directly in the serializer
        serializer.validated_data['author_id'] = user_id  # Assuming 'author_id' is the correct field in your serializer
        serializer.save(post_id=self.kwargs['post_id'])

        return Response({'status': 'success', 'message': 'Comment created successfully'}, status=status.HTTP_201_CREATED)





