
import os
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key (sempre manter em segredo)
SECRET_KEY = 'y8w0(32r68=x2d7(7wdnl_qagab3d5#4jb_aki(!##t)+01ak+'

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Debug (desabilitar em produção)
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Definindo o modelo de usuário customizado
AUTH_USER_MODEL = 'users.CustomUser'

# Redirecionamento após login e logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Aplicativos instalados
INSTALLED_APPS = [
    'app',
    'dashboard',
    'users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',

]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'daily.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'daily.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'iBvElZhlNMfYStNyXHOlReSUYpMtjuGt',
        'HOST': 'maglev.proxy.rlwy.net',
        'PORT': '25532',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# Configuração do CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

# Session/Cookie
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'


# Configuração de API Externa
EXTERNAL_API_BASE_URL = 'https://api-1-4c9f.onrender.com/'
EXTERNAL_API_REGISTER_URL = EXTERNAL_API_BASE_URL + 'api/TodoItem'

# Localização e Idioma
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Arquivos estáticos
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app/static'),  
    os.path.join(BASE_DIR, 'dashboard/static'),  
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


#LOGGING = {
    #'version': 1,
    #'handlers': {
        #'console': {
            #'class': 'logging.StreamHandler',
        #},
    #},
    #'loggers': {
       # 'django': {
        #    'handlers': ['console'],
        #    'level': 'DEBUG',
        #},
    #},
#}