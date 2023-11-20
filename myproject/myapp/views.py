# myapp/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import timedelta 
from django.shortcuts import get_object_or_404
from traceback import print_exc
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Post, Comment
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
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
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                access_token.set_exp(lifetime=timedelta(hours=10))  
                token_payload = {
                    'token': str(access_token),
                    'user_id': user.id,
                }

                return Response({'status': 'success', 'data': token_payload})
            else:
                return Response({'status': 'error', 'message': 'Invalid login credentials'})
        except Exception as e:
            print_exc()  
            return Response({'status': 'error', 'message': 'An error occurred during login'})
    else:
        return Response({'status': 'error', 'message': 'Invalid request method'})

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        token = self.request.auth
        user_id = token.payload.get('user_id')
        queryset = Post.objects.filter(author_id=user_id)
        return queryset

    def perform_create(self, serializer):
        token = self.request.auth
        user_id = token.payload.get('user_id')
        serializer.validated_data['author_id'] = user_id  
        serializer.save()

        return Response({'status': 'success', 'message': 'Post created successfully'}, status=status.HTTP_201_CREATED)


class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        token = request.auth
        user_id = token.payload.get('user_id')
        post = get_object_or_404(Post, pk=pk)

        if user_id == post.author.id:
            post.delete()
            return Response({'status': 'success', 'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'Permission denied. User is not the owner of the post.'}, status=status.HTTP_403_FORBIDDEN)



class PostUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, post_id):

        token = request.auth
        user_id = token.payload.get('user_id')
        post = get_object_or_404(Post, pk=post_id)
        if user_id == post.author.id:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error', 'message': 'Permission denied. User is not the owner of the post.'}, status=status.HTTP_403_FORBIDDEN)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        token = self.request.auth
        user_id = token.payload.get('user_id')
        serializer.validated_data['author_id'] = user_id  
        serializer.save(post_id=self.kwargs['post_id'])

        return Response({'status': 'success', 'message': 'Comment created successfully'}, status=status.HTTP_201_CREATED)





