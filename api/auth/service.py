from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class AuthService():
    def login(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password') 
            
            if not email or not password:
                return Response({'message': 'no email or password was passed'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'invalid credentials'}, status = status.HTTP_400_BAD_REQUEST)
            
            user = authenticate(username=user.username, password=password)
            if user is not None:
                refresh_token = RefreshToken.for_user(user)
                access_token = str(refresh_token.access_token)
                
                return Response({
                    'message': 'success',
                    'access_token': access_token
                }, status=status.HTTP_200_OK)
            return Response({"message": 'error'})
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)