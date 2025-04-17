# Daily Guide

**Daily Guide** é um projeto web desenvolvido com Django, focado em gerenciamento diário de tarefas e metas. O sistema inclui autenticação de usuários com páginas de login personalizadas utilizando Bootstrap.

## 🚀 Funcionalidades

- ✅ Sistema de login de usuários
- ✅ Layout moderno e responsivo com Bootstrap
- ✅ Validação de formulários
- ✅ Redirecionamento para dashboard após login

## 🛠 Tecnologias utilizadas

- Python
- Django
- Dotnet
- Postgres
- Docker
- Bootstrap 5
- HTML e CSS

## 📦 Como executar o projeto

```bash
# Clone o repositório
git clone https://github.com/Adalbert-s/Daily-Guide.git
cd Daily-Guide

# Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/macOS

# Instale as dependências
pip install -r requirements.txt

# Aplique as migrações
python manage.py migrate

# Execute o servidor
python manage.py runserver
