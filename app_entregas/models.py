from django.db import models
from django.contrib.auth.models import User

class StatusEntrega(models.TextChoices):
    PENDENTE_ROTA = 'PENDENTE_ROTA', 'Pendente de Rota'
    DISPONIVEL = 'DISPONIVEL', 'Disponível'
    ACEITA = 'ACEITA', 'Aceita'
    COLETADA = 'COLETADA', 'Coletada'
    ENTREGUE = 'ENTREGUE', 'Entregue'
    CANCELADA = 'CANCELADA', 'Cancelada' # <-- Já estava aí, mas precisamos usar

class StatusRota(models.TextChoices):
    EM_MONTAGEM = 'EM_MONTAGEM', 'Em Montagem'
    DISPONIVEL = 'DISPONIVEL', 'Disponível'
    ACEITA = 'ACEITA', 'Aceita'
    EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em Andamento'
    CONCLUIDA = 'CONCLUIDA', 'Concluída'

class Loja(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_fantasia = models.CharField(max_length=100)
    endereco_retirada = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome_fantasia

class Entregador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    veiculo = models.CharField(max_length=50)
    disponivel = models.BooleanField(default=True) # Mudei para True por padrão para facilitar testes
    
    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

class Rota(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    entregador = models.ForeignKey(Entregador, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusRota.choices, default=StatusRota.EM_MONTAGEM)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_aceite = models.DateTimeField(null=True, blank=True) # <-- NOVO: Data do aceite
    
    def __str__(self):
        return f"Rota #{self.id} - {self.loja.nome_fantasia}"

class Entrega(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    rota = models.ForeignKey(Rota, on_delete=models.SET_NULL, null=True, blank=True)
    destinatario = models.CharField(max_length=100)
    endereco_destino = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusEntrega.choices, default=StatusEntrega.PENDENTE_ROTA)
    
    # NOVOS CAMPOS DE DATAS EXIGIDOS PELO PDF
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    data_coleta = models.DateTimeField(null=True, blank=True)
    data_entrega = models.DateTimeField(null=True, blank=True)
    data_cancelamento = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Entrega {self.id} - {self.destinatario}"