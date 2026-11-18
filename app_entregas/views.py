from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import EntregaForm
from .models import Loja, Entrega, Rota, Entregador

#Tela de Cadastro de Usuário
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'app_entregas/cadastro.html'

#Tela do Painel Dashboard
@login_required
def dashboard(request):
    is_loja = Loja.objects.filter(usuario=request.user).exists()
    is_entregador = Entregador.objects.filter(usuario=request.user).exists()
    return render(request, 'app_entregas/dashboard.html', {'is_loja': is_loja, 'is_entregador': is_entregador})

#Tela de Cadastrar Pedido
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

#tela de Listar Pedidos 
@login_required
def listar_pedidos(request):
    try:
        loja = Loja.objects.get(usuario=request.user)
        pedidos = Entrega.objects.filter(loja=loja).order_by('-data_solicitacao')
    except Loja.DoesNotExist:
        pedidos = []
    return render(request, 'app_entregas/listar_pedidos.html', {'pedidos': pedidos})

#Ação de Cancelar Pedido
@login_required
def cancelar_pedido(request, entrega_id):
    pedido = get_object_or_404(Entrega, id=entrega_id, loja__usuario=request.user)
    
    if pedido.status in ['PENDENTE_ROTA', 'DISPONIVEL']:
        pedido.status = 'CANCELADA'
        pedido.data_cancelamento = timezone.now()
        
        if pedido.rota:
            rota = pedido.rota
            pedido.rota = None
            pedido.save()
            
            if rota.entrega_set.count() == 0:
                rota.status = 'EM_MONTAGEM'
                rota.save()
        else:
            pedido.save()
            
    return redirect('listar_pedidos')

#Ação de Criar Rota Agrupada
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

#Ação de Criar Rota Individual 
@login_required
def criar_rota_individual(request, entrega_id):
    pedido = get_object_or_404(Entrega, id=entrega_id, loja__usuario=request.user)
    if pedido.status == 'PENDENTE_ROTA':
        nova_rota = Rota.objects.create(loja=pedido.loja, status='DISPONIVEL')
        pedido.rota = nova_rota
        pedido.status = 'DISPONIVEL'
        pedido.save()
    return redirect('listar_pedidos')

#Tela de Rotas Disponíveis
@login_required
def listar_rotas(request):
    rotas = Rota.objects.filter(status='DISPONIVEL')
    return render(request, 'app_entregas/rotas_disponiveis.html', {'rotas': rotas})

#Ação de Aceitar Rota
@login_required
def aceitar_rota(request, rota_id):
    rota = get_object_or_404(Rota, id=rota_id)
    
    entregador, created = Entregador.objects.get_or_create(
        usuario=request.user, defaults={'veiculo': 'Não informado', 'disponivel': True}
    )
    
    tem_rota_ativa = Rota.objects.filter(entregador=entregador, status__in=['ACEITA', 'EM_ANDAMENTO']).exists()
    
    if not entregador.disponivel or tem_rota_ativa:
        return redirect('minhas_rotas') 
        
    if rota.status == 'DISPONIVEL':
        rota.entregador = entregador
        rota.status = 'ACEITA'
        rota.data_aceite = timezone.now()
        rota.save()
        # O entregador fica indisponível ao aceitar uma rota
        entregador.disponivel = False
        entregador.save()
        
        for pedido in rota.entrega_set.all():
            pedido.status = 'ACEITA'
            pedido.save()
            
    return redirect('listar_rotas')

#Tela de Minhas Rotas Ativas
@login_required
def minhas_rotas(request):
    entregador = Entregador.objects.filter(usuario=request.user).first()
    rotas = Rota.objects.filter(entregador=entregador).exclude(status='CONCLUIDA').order_by('-data_criacao') if entregador else []
    return render(request, 'app_entregas/minhas_rotas.html', {'rotas': rotas})

#Ação de Coletar 
@login_required
def acao_entrega(request, entrega_id, acao):
    pedido = get_object_or_404(Entrega, id=entrega_id, rota__entregador__usuario=request.user)
    
    if acao == 'coletar' and pedido.status == 'ACEITA':
        pedido.status = 'COLETADA'
        pedido.data_coleta = timezone.now()
        pedido.save() 
        
        pedido.rota.status = 'EM_ANDAMENTO'
        pedido.rota.save()
        
    elif acao == 'entregar' and pedido.status == 'COLETADA':
        pedido.status = 'ENTREGUE'
        pedido.data_entrega = timezone.now()
        pedido.save() 
        
        todos_entregues = all(p.status == 'ENTREGUE' for p in pedido.rota.entrega_set.all())
        if todos_entregues:
            pedido.rota.status = 'CONCLUIDA'
            pedido.rota.save()
             # Libera o entregador para novas rotas
            entregador = pedido.rota.entregador
            if entregador:
                entregador.disponivel = True
                entregador.save()
            
    return redirect('minhas_rotas')

#Ação de Alternar Disponibilidade
@login_required
def alternar_disponibilidade(request):
    entregador = Entregador.objects.filter(usuario=request.user).first()
    if entregador:
        # Não deixa ficar disponível se estiver com rota em andamento
        tem_rota_ativa = Rota.objects.filter(entregador=entregador, status__in=['ACEITA', 'EM_ANDAMENTO']).exists()
        if not tem_rota_ativa:
            entregador.disponivel = not entregador.disponivel
            entregador.save()
    return redirect('dashboard')

#Histórico da Loja
@login_required
def historico_loja(request):
    try:
        loja = Loja.objects.get(usuario=request.user)
        entregas_concluidas = Entrega.objects.filter(loja=loja, status='ENTREGUE').order_by('-data_solicitacao')
    except Loja.DoesNotExist:
        entregas_concluidas = []
    return render(request, 'app_entregas/historico_loja.html', {'entregas': entregas_concluidas})

#Histórico do Entregador
@login_required
def historico_entregador(request):
    entregador = Entregador.objects.filter(usuario=request.user).first()
    if entregador:
        rotas_concluidas = Rota.objects.filter(entregador=entregador, status='CONCLUIDA').order_by('-data_criacao')
    else:
        rotas_concluidas = []
    return render(request, 'app_entregas/historico_entregador.html', {'rotas': rotas_concluidas})
