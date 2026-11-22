from django.db import models
from django.contrib.auth.models import User

# ENUMS TextChoices
# Garantem a integridade dos status do sistema
# Evita que alguém digite "entregue" ou "Entregue" no banco e quebre o sistema
class StatusEntrega(models.TextChoices):
    PENDENTE_ROTA = 'PENDENTE_ROTA', 'Pendente de Rota'
    DISPONIVEL = 'DISPONIVEL', 'Disponível'
    ACEITA = 'ACEITA', 'Aceita'
    COLETADA = 'COLETADA', 'Coletada'
    ENTREGUE = 'ENTREGUE', 'Entregue'
    CANCELADA = 'CANCELADA', 'Cancelada' 

class StatusRota(models.TextChoices):
    EM_MONTAGEM = 'EM_MONTAGEM', 'Em Montagem'
    DISPONIVEL = 'DISPONIVEL', 'Disponível'
    ACEITA = 'ACEITA', 'Aceita'
    EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em Andamento'
    CONCLUIDA = 'CONCLUIDA', 'Concluída'

# ENTIDADES DO SISTEMA

class Loja(models.Model):
    #Relacionamento 1 para 1 com o usuário de autenticação do Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_fantasia = models.CharField(max_length=100)
    #O endereço de retirada é salvo no pedido para preservar o histórico 
    endereco_retirada = models.CharField(max_length=255)
    
    def __str__(self):
        #Define como o objeto será exibido no painel Admin
        return self.nome_fantasia

class Entregador(models.Model):
    #Relacionamento 1 para 1 com o usuário de autenticação do Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    veiculo = models.CharField(max_length=50)
    #Controla se o entregador pode aceitar novas rotas
    disponivel = models.BooleanField(default=True) 

    def __str__(self):
        #Se tiver nome completo cadastrado usa, se não usa o username
        return self.usuario.get_full_name() or self.usuario.username

class Rota(models.Model):
    #Uma loja pode ter várias rotas
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    #A rota pode não ter entregador (null/blank) até ser aceita 
    #Se o entregador for deletado do banco, a rota não é apagada, fica como null (SET_NULL)
    entregador = models.ForeignKey(Entregador, on_delete=models.SET_NULL, null=True, blank=True)
    #O status inicial de toda rota é Em Montagem 
    status = models.CharField(max_length=20, choices=StatusRota.choices, default=StatusRota.EM_MONTAGEM)
    data_criacao = models.DateTimeField(auto_now_add=True)
    #Grava o momento exato do aceite para o histórico 
    data_aceite = models.DateTimeField(null=True, blank=True) 
    
    def __str__(self):
        return f"Rota #{self.id} - {self.loja.nome_fantasia}"

class Entrega(models.Model):
    #Cada pedido pertence a uma única loja 
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    #O pedido pode estar sem rota (null/blank) enquanto aguarda organização 
    rota = models.ForeignKey(Rota, on_delete=models.SET_NULL, null=True, blank=True)
    
    destinatario = models.CharField(max_length=100)
    endereco_destino = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    #Status inicial é Pendente de Rota (RN 005)
    status = models.CharField(max_length=20, choices=StatusEntrega.choices, default=StatusEntrega.PENDENTE_ROTA)
    

    # CAMPOS DE DATA (Para o Histórico)
    
    data_solicitacao = models.DateTimeField(auto_now_add=True) #Preenchido ao criar
    data_coleta = models.DateTimeField(null=True, blank=True) #Preenchido ao coletar
    data_entrega = models.DateTimeField(null=True, blank=True) #Preenchido ao entregar
    data_cancelamento = models.DateTimeField(null=True, blank=True)#Preenchido ao cancelar
    
    def __str__(self):
        return f"Entrega {self.id} - {self.destinatario}"