"""
Configurações do projeto Entrega+.
Este arquivo centraliza todas as configurações de segurança, banco de dados, 
idioma e arquivos estáticos do sistema.
"""

from pathlib import Path
import os
import dj_database_url

#Define o diretório base do projeto onde fica o manage.py
BASE_DIR = Path(__file__).resolve().parent.parent

#CHAVE Usada para criptografia de sessões e senhas.
# Em um sistema  profissional isso deveria vir de uma variável de ambiente por segurança é claro 
SECRET_KEY = 'django-insecure-)0atn(+qv#2bb-621dd%&0g(9k+tyzgyf3dqhnyb#h1+%h(@m_'

# MODO DEBUG Fica False por padrão. Só é True se você definir a variável de ambiente DEBUG=True no seu PC
# Isso garante que o site no Render não exponha detalhes de erros para os usuários
# o Render ele é um serviço de hospedagem na nuvem que permite hospedar aplicativos web, incluindo projetos Django, 
# facilitando o deploy e a escalabilidade de aplicações web. Ele oferece recursos como gerenciamento de banco de dados, 
# integração contínua, monitoramento e suporte a várias linguagens de programação, tornando-o uma opção  para
# desenvolvedores que desejam implantar e gerenciar suas aplicações na nuvem

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# HOSTS PERMITIDOS só avisa o Django quem pode acessar o site 
# Aceita o localhost seu PC e qualquer subdomínio do Render produção
ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

# APPS INSTALADOS: Módulos nativos do Django e o nosso app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_entregas',
    'rest_framework',    
    'drf_spectacular',    
]
# MIDDLEWARES: Camadas de segurança e processamento que cada requisição passa.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--Essencial para servir CSS no Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'entrega_mais.urls'

#Configuração dos Templates HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True, #Permite que o Django ache a pasta 'templates' dentro do app_entregas
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'entrega_mais.wsgi.application'

# BANCO DE DADOS (A Mágica Local x Nuvem)
# Usamos a biblioteca dj_database_url
# Se existir a variável DATABASE_URL (no Render) ele usa o PostgreSQL
# Se não existir no seu PC ele usa o SQLite (sqlite:///db.sqlite3)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}

# Validações de segurança de senha nativas do Django
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNACIONALIZAÇÃO Localização
LANGUAGE_CODE = 'pt-br' #Traduz o painel Admin para Português br
TIME_ZONE = 'America/Campo_Grande' # Fuso horário do Mato Grosso do Sul (UTC-4)
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
# STATIC_ROOT: Pasta onde o collectstatic vai juntar os arquivos CSS para o Render ler
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
# STORAGE: Comprime e otimiza os arquivos estáticos no deploy
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 

# Configuração de e-mail padrão para desenvolvimento mostra no terminal
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# Para onde o usuário é redirecionado após fazer login
LOGIN_REDIRECT_URL = '/dashboard/'

# CONFIGURAÇÕES DE SEGURANÇA PARA DEPLOY RENDER
# Origens confiáveis para envio de formulários evita erro CSRF no Render
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://*.onrender.com", 
]

# Em produção real com HTTPS, esses valores deveriam ser True
# Como o plano free do Render às vezes redireciona ou testamos em HTTP local, mantemos False para evitar problemas de cookies
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Entrega+ API',
    'DESCRIPTION': 'API para o Sistema de Gerenciamento de Entregas',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}