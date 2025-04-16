import requests

# URL da API de usuários em C#
api_url = 'http://localhost:5000/api/users'  # Verifique se o seu servidor da API está rodando nessa porta

def create_user_in_api(name, email, password):
    data = {
        "name": name,
        "email": email,
        "password": password
    }

    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()  # Lança uma exceção se o status code não for 2xx
        return response.json()  # Retorna a resposta (usuário criado)
    except requests.exceptions.RequestException as e:
        return str(e)  # Em caso de erro, retorna a mensagem de erro
