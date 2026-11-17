from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

# Importando TODAS as views que criamos
from app_entregas.views import (
    SignUpView, dashboard, cadastrar_pedido, listar_pedidos,
    criar_rota, criar_rota_individual, listar_rotas,
    aceitar_rota, minhas_rotas, acao_entrega, resetar_teste
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='app_entregas/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='app_entregas/login.html'), name='login'),
    path('cadastro/', SignUpView.as_view(), name='cadastro'),
    
    # Painel e Pedidos da Loja
    path('dashboard/', dashboard, name='dashboard'),
    path('pedido/novo/', cadastrar_pedido, name='cadastrar_pedido'),
    path('meus-pedidos/', listar_pedidos, name='listar_pedidos'),
    
    # Rotas (Criação pela Loja)
    path('rotas/criar/', criar_rota, name='criar_rota'),
    path('rotas/criar/<int:entrega_id>/', criar_rota_individual, name='criar_rota_individual'),
    
    # Rotas (Ações do Entregador)
    path('rotas/', listar_rotas, name='listar_rotas'),
    path('rotas/aceitar/<int:rota_id>/', aceitar_rota, name='aceitar_rota'),
    path('minhas-rotas/', minhas_rotas, name='minhas_rotas'),
    path('entrega/<int:entrega_id>/<str:acao>/', acao_entrega, name='acao_entrega'),
    
    # Utilitário de teste
    path('reset/', resetar_teste, name='resetar_teste'),
]