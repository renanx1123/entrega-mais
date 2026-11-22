"""
ASGI config for entrega_mais project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Define o arquivo de configurações padrão do projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entrega_mais.settings')

# Cria a aplicação ASGI
# Nota Para o deploy no Render nós usamos o WSGI (wsgi.py) com o Gunicorn
# mas esse arquivo ASGI é mantido caso o projeto precise de recursos assíncronos no futuro é claro
#  que o Django já suporta isso nativamente, mas para o deploy no Render é necessário usar o WSGI
application = get_asgi_application()