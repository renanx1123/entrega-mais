from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

# Imports do Swagger (drf-spectacular)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

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
    
    path('', auth_views.LoginView.as_view(template_name='app_entregas/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='app_entregas/login.html'), name='login'),
    path('cadastro/', SignUpView.as_view(), name='cadastro'),
    
    # PAINEL PRINCIPAL (DASHBOARD)
    path('dashboard/', dashboard, name='dashboard'),
    
    # ROTAS DA LOJA (RF 004, 005, 012, 013)
    path('pedido/novo/', cadastrar_pedido, name='cadastrar_pedido'),
    path('meus-pedidos/', listar_pedidos, name='listar_pedidos'),
    path('pedido/cancelar/<int:entrega_id>/', cancelar_pedido, name='cancelar_pedido'),
    path('rotas/criar/', criar_rota, name='criar_rota'),
    path('rotas/criar/<int:entrega_id>/', criar_rota_individual, name='criar_rota_individual'),
    
    # ROTAS DO ENTREGADOR (RF 007, 008, 009, 010, 011)
    path('rotas/', listar_rotas, name='listar_rotas'),
    path('rotas/aceitar/<int:rota_id>/', aceitar_rota, name='aceitar_rota'),
    path('minhas-rotas/', minhas_rotas, name='minhas_rotas'),
    path('entrega/<int:entrega_id>/<str:acao>/', acao_entrega, name='acao_entrega'),
    path('entregador/disponibilidade/', alternar_disponibilidade, name='alternar_disponibilidade'), 
    
    # HISTÓRICOS (RF 014, 015)
    path('historico-loja/', historico_loja, name='historico_loja'),
    path('historico-entregador/', historico_entregador, name='historico_entregador'),
    
    # ROTAS DA API (SWAGGER)
    # Gera o esquema da API (JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Interface visual do Swagger
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # UTILITÁRIO DE DESENVOLVIMENTO
    path('reset/', resetar_teste, name='resetar_teste'),
]