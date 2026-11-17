from django import forms
from .models import Entrega

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        # Vamos pedir os dados básicos do pedido. 
        # O 'loja' e o 'status' nós preencheremos automaticamente no código.
        fields = ['destinatario', 'endereco_destino', 'telefone']
        
        # Deixando os campos mais bonitos
        widgets = {
            'destinatario': forms.TextInput(attrs={'placeholder': 'Nome de quem vai receber'}),
            'endereco_destino': forms.TextInput(attrs={'placeholder': 'Rua, número, bairro...'}),
            'telefone': forms.TextInput(attrs={'placeholder': 'Ex: (67) 99999-9999'}),
        }