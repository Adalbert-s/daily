import requests
from django.conf import settings
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from .serializers import LoginSerializer
from django.contrib.auth import authenticate


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
        except IntegrityError:
            return Response(
                {"detail": "Erro ao salvar o usuario."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Envia os dados para a API externa
        response = requests.post(settings.EXTERNAL_API_REGISTER_URL, json={
            'nome': username,
            'email': email,
            'senha': password,
        })

        if response.status_code == 201:
            return Response({"message": "Usuario criado com sucesso"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail": "Falha ao criar usuario na API externa"},
                status=status.HTTP_400_BAD_REQUEST
            )

class LoginView(APIView):
    def post(self, request):
        # Valida os dados recebidos com o serializer
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Tenta autenticar o usuario com o Django
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Se o usuario for autenticado com sucesso, envia os dados para a API externa
            response = requests.post(settings.EXTERNAL_API_LOGIN_URL, data={
                'Nome': username,
                'Senha': password,
            })

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "Falha ao autenticar com a API externa"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Caso o usuario não seja encontrado ou a senha esteja incorreta
        return Response(
            {"detail": "Credenciais invalidas ou falha na autenticacao"},
            status=status.HTTP_400_BAD_REQUEST
        )