from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer

User = get_user_model()

class Register(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Esse nome de usuario ja esta em uso."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = serializer.save()
            token = Token.objects.create(user=user)
        except IntegrityError:
            return Response(
                {"detail": "Erro ao salvar o usuario."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            "message": "Usuario criado com sucesso",
            "token": token.key
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "message": "Login bem-sucedido",
                "token": token.key
            }, status=status.HTTP_200_OK)

        return Response(
            {"detail": "Credenciais invalidas ou falha na autenticacao"},
            status=status.HTTP_400_BAD_REQUEST
        )
