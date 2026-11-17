from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import EntregaForm
from .models import Loja, Entrega, Rota, Entregador

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app_entregas/cadastro.html'

@login_required
def dashboard(request):
    is_loja = Loja.objects.filter(usuario=request.user).exists()
    is_entregador = Entregador.objects.filter(usuario=request.user).exists()
    return render(request, 'app_entregas/dashboard.html', {'is_loja': is_loja, 'is_entregador': is_entregador})

@login_required
def cadastrar_pedido(request):
    if request.method == 'POST':
        form = EntregaForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            loja, created = Loja.objects.get_or_create(
                usuario=request.user, 
                defaults={'nome_fantasia': request.user.username, 'endereco_retirada': 'Endereço Padrão'}
            )
            pedido.loja = loja
            pedido.save()
            return redirect('dashboard')
    else:
        form = EntregaForm()
    return render(request, 'app_entregas/cadastrar_pedido.html', {'form': form})

@login_required
def listar_pedidos(request):
    try:
        loja = Loja.objects.get(usuario=request.user)
        pedidos = Entrega.objects.filter(loja=loja).order_by('-data_solicitacao')
    except Loja.DoesNotExist:
        pedidos = []
    return render(request, 'app_entregas/listar_pedidos.html', {'pedidos': pedidos})

# Criar rota agrupada (Botão de cima)
@login_required
def criar_rota(request):
    try:
        loja = Loja.objects.get(usuario=request.user)
    except Loja.DoesNotExist:
        return redirect('dashboard')

    pedidos_pendentes = Entrega.objects.filter(loja=loja, status='PENDENTE_ROTA')
    if pedidos_pendentes.exists():
        nova_rota = Rota.objects.create(loja=loja, status='DISPONIVEL')
        for pedido in pedidos_pendentes:
            pedido.rota = nova_rota
            pedido.status = 'DISPONIVEL'
            pedido.save()
    return redirect('listar_pedidos')

# Criar rota individual (Botão de cada pedido)
@login_required
def criar_rota_individual(request, entrega_id):
    pedido = get_object_or_404(Entrega, id=entrega_id, loja__usuario=request.user)
    if pedido.status == 'PENDENTE_ROTA':
        nova_rota = Rota.objects.create(loja=pedido.loja, status='DISPONIVEL')
        pedido.rota = nova_rota
        pedido.status = 'DISPONIVEL'
        pedido.save()
    return redirect('listar_pedidos')

@login_required
def listar_rotas(request):
    rotas = Rota.objects.filter(status='DISPONIVEL')
    return render(request, 'app_entregas/rotas_disponiveis.html', {'rotas': rotas})

@login_required
def aceitar_rota(request, rota_id):
    rota = get_object_or_404(Rota, id=rota_id)
    if rota.status == 'DISPONIVEL':
        entregador, created = Entregador.objects.get_or_create(
            usuario=request.user, defaults={'veiculo': 'Não informado', 'disponivel': False}
        )
        rota.entregador = entregador
        rota.status = 'ACEITA'
        rota.save()
        
        for pedido in rota.entrega_set.all():
            pedido.status = 'ACEITA'
            pedido.save()
    return redirect('listar_rotas')

# NOVO: Tela de Minhas Rotas (O que o Entregador aceitou)
@login_required
def minhas_rotas(request):
    entregador = Entregador.objects.filter(usuario=request.user).first()
    rotas = Rota.objects.filter(entregador=entregador).exclude(status='CONCLUIDA').order_by('-data_criacao') if entregador else []
    return render(request, 'app_entregas/minhas_rotas.html', {'rotas': rotas})

# NOVO: Ação do Entregador (Coletar ou Entregar)
@login_required
def acao_entrega(request, entrega_id, acao):
    pedido = get_object_or_404(Entrega, id=entrega_id, rota__entregador__usuario=request.user)
    
    if acao == 'coletar' and pedido.status == 'ACEITA':
        pedido.status = 'COLETADA'
        # Atualiza a rota para EM_ANDAMENTO se for a primeira coleta
        pedido.rota.status = 'EM_ANDAMENTO'
        pedido.rota.save()
        
    elif acao == 'entregar' and pedido.status == 'COLETADA':
        pedido.status = 'ENTREGUE'
        
        # Verifica se todos os pedidos da rota foram entregues para concluir a rota
        todos_entregues = all(p.status == 'ENTREGUE' for p in pedido.rota.entrega_set.all())
        if todos_entregues:
            pedido.rota.status = 'CONCLUIDA'
            pedido.rota.save()
            
    pedido.save()
    return redirect('minhas_rotas')

@login_required
def resetar_teste(request):
    Entrega.objects.all().update(rota=None, status='PENDENTE_ROTA')
    Rota.objects.all().delete()
    return redirect('dashboard')