from django.contrib import admin
from .models import Loja, Entregador, Rota, Entrega

# O admin.py faz a parte de  registrar os modelos no painel de administração do Django.
# É com esse arquivo que o administrador perfil criado com createsuperuser
# consegue visualizar, adicionar, editar e deletar os dados das tabelas

admin.site.register(Loja)       # Habilita a gestão de Lojas no painel
admin.site.register(Entregador) # Habilita a gestão de Entregadores no painel
admin.site.register(Rota)       # Habilita a visualização e edição de Rotas
admin.site.register(Entrega)    # Habilita a visualização e edição de Pedidos/Entregas