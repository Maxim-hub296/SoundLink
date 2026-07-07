from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)  # Создание Refesh и Access
            refresh.payload.update({  # Полезная информация в самом токене
                'user_id': user.id,
                'username': user.username
            })

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),  # Отправка на клиент
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None or password is None:
            return Response({'error': 'Нужен и логин, и пароль'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Неверные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            "username": user.username
        })
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token', None)
        if not refresh_token:
            return Response({
                "error": "Необходим Refresh Token"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({
                "error": "Неверный Refresh Token"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "success": "Выход успешен"
        }, status=status.HTTP_200_OK)
