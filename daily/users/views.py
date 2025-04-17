import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            nome = serializer.validated_data['username']
            senha = serializer.validated_data['password']

            # Enviar os dados para a API externa para login
            response = requests.post(settings.EXTERNAL_API_LOGIN_URL, data={
                'Nome': nome,
                'Senha': senha,
            })

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Credenciais invalidas ou falha na autenticacao"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class Register(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Enviar os dados do usuário para a API externa
            response = requests.post(settings.EXTERNAL_API_REGISTER_URL, data={
                'Nome': user.username,   # Enviar o nome do usuário
                'Email': user.email,     # Enviar o email
                'Senha': user.password,  # Enviar a senha (cuidado com a segurança)
            })

            if response.status_code == 201:
                return Response({"message": "Usuario criado com sucesso"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Falha ao criar usuario na API externa"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
