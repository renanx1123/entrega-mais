from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

# Importação de todas as Views funções que criamos no app_entregas
from app_entregas.views import (
    SignUpView, dashboard, cadastrar_pedido, listar_pedidos,
    criar_rota, criar_rota_individual, listar_rotas,
    aceitar_rota, minhas_rotas, acao_entrega, resetar_teste,
    historico_loja, historico_entregador, cancelar_pedido,
    alternar_disponibilidade
)

urlpatterns = [
    # PAINEL ADMINISTRATIVO E AUTENTICAÇÃO
    path('admin/', admin.site.urls),
    
    # Tela de Login  Utiliza a view nativa do Django
    path('', auth_views.LoginView.as_view(template_name='app_entregas/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='app_entregas/login.html'), name='login'),
    
    # Tela de Cadastro
    path('cadastro/', SignUpView.as_view(), name='cadastro'),
    
    # PAINEL PRINCIPAL (DASHBOARD)
    path('dashboard/', dashboard, name='dashboard'),
    
    # ROTAS DA LOJA 
    path('pedido/novo/', cadastrar_pedido, name='cadastrar_pedido'),
    path('meus-pedidos/', listar_pedidos, name='listar_pedidos'),
    
    # O <int:entrega_id> passa o ID do pedido para a View, permitindo cancelar ou enviar apenas aquele pedido específico
    path('pedido/cancelar/<int:entrega_id>/', cancelar_pedido, name='cancelar_pedido'),
    path('rotas/criar/', criar_rota, name='criar_rota'),
    path('rotas/criar/<int:entrega_id>/', criar_rota_individual, name='criar_rota_individual'),
    
    # ROTAS DO ENTREGADOR
    path('rotas/', listar_rotas, name='listar_rotas'),
    
    # <int:rota_id> identifica qual rota o entregador está tentando aceitar.
    path('rotas/aceitar/<int:rota_id>/', aceitar_rota, name='aceitar_rota'),
    
    path('minhas-rotas/', minhas_rotas, name='minhas_rotas'),
    
    # <str:acao> recebe uma string ('coletar' ou 'entregar') para saber qual botão foi clicado.
    path('entrega/<int:entrega_id>/<str:acao>/', acao_entrega, name='acao_entrega'),
    
    path('entregador/disponibilidade/', alternar_disponibilidade, name='alternar_disponibilidade'), 
    
    # HISTÓRICOS
    path('historico-loja/', historico_loja, name='historico_loja'),
    path('historico-entregador/', historico_entregador, name='historico_entregador'),
        # UTILITÁRIO DE DESENVOLVIMENTO
    # Botão para limpar o banco de dados de testes novamente vou falar esse botão é só para desenvolvimento e testes,
    #  não deve existir em versões futuras
    path('reset/', resetar_teste, name='resetar_teste'),
]