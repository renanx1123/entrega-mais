from django.db import models
from django.contrib.auth.models import User

# --- STATUS DEFINIDOS NAS REGRAS DE NEGÓCIO ---
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

# --- ENTIDADES ---

class Loja(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_fantasia = models.CharField(max_length=100)
    endereco_retirada = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome_fantasia

class Entregador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    veiculo = models.CharField(max_length=50)
    disponivel = models.BooleanField(default=False) # RN 009
    
    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

class Rota(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    entregador = models.ForeignKey(Entregador, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusRota.choices, default=StatusRota.EM_MONTAGEM)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Rota #{self.id} - {self.loja.nome_fantasia}"

class Entrega(models.Model): # Antigo "Pedido"
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    rota = models.ForeignKey(Rota, on_delete=models.SET_NULL, null=True, blank=True) # RN 003
    destinatario = models.CharField(max_length=100)
    endereco_destino = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusEntrega.choices, default=StatusEntrega.PENDENTE_ROTA)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Entrega {self.id} - {self.destinatario}"