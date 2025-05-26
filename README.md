# Daily Guide

**Daily Guide** é um projeto web desenvolvido com Django, focado em gerenciamento diário de tarefas, agendas e metas. O sistema inclui autenticação de usuários com páginas de login personalizadas utilizando Bootstrap, além de um dashboard para visualização e organização das tarefas.

## 🚀 Funcionalidades

- ✅ Sistema de login e cadastro de usuários  
- ✅ Layout moderno e responsivo com Bootstrap  
- ✅ Validação de formulários  
- ✅ Redirecionamento para dashboard após login  
- ✅ Criação, edição e exclusão de tarefas  
- ✅ Organização de tarefas em agendas e categorias  
- ✅ Dashboard com visualização das tarefas do dia  

## 🛠 Tecnologias utilizadas

- Python  
- Django  
- Bootstrap 5  
- HTML e CSS   

## 📦 Como executar o projeto

### 1. Clone o repositório


git clone https://github.com/Adalbert-s/Daily-Guide.git
cd Daily-Guide
2. Instale o Poetry (se ainda não tiver)
bash
Copiar
Editar
pip install poetry
Nota: O Poetry é uma ferramenta para gerenciamento de dependências e ambientes virtuais em Python.
Mais informações em https://python-poetry.org/docs/#installation

3. Instale as dependências e crie o ambiente virtual
bash
Copiar
Editar
poetry install
4. Ative o ambiente virtual
bash
Copiar
Editar
poetry shell
5. Aplique as migrações do banco de dados
bash
Copiar
Editar
python manage.py migrate
6. Execute o servidor de desenvolvimento
bash
Copiar
Editar
python manage.py runserver
Agora acesse http://localhost:8000 no seu navegador.

🚀 Como rodar em produção (exemplo básico)
1. Gere os arquivos estáticos
bash
Copiar
Editar
python manage.py collectstatic
2. Instale o Gunicorn (se não estiver instalado)
bash
Copiar
Editar
poetry add gunicorn
3. Rode o servidor com Gunicorn (exemplo)
bash
Copiar
Editar
gunicorn daily.wsgi:application --bind 0.0.0.0:8000
Você pode usar servidores web como Nginx para fazer proxy reverso e configurar HTTPS em produção.

📚 Uso
Acesse http://localhost:8000 no navegador

Faça cadastro/login

Use o dashboard para gerenciar suas tarefas e agendas

🤝 Contribuição
Sinta-se livre para abrir issues e enviar pull requests. Toda contribuição é bem-vinda!

📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

