from django import forms
from .models import Entrega

# O forms.py é ele que faz a parte de  criar os formulários HTML de forma automatizada.
# Usamos o 'ModelForm', que se conecta diretamente ao banco de dados models.py
class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        

        # incluímos os campos que o usuário pode digitar (destinatário, endereço e telefone)
        # Os campos loja e status não estão aqui porque eles são preenchidos logicamente kk
        # automaticamente pelo sistema nas Views. Isso impede que um usuário mal-intencionado
        # tente forjar um formulário para criar pedidos em nome de outra loja.
        fields = ['destinatario', 'endereco_destino', 'telefone']
        
        widgets = {
            'destinatario': forms.TextInput(attrs={'placeholder': 'Nome de quem vai receber'}),
            'endereco_destino': forms.TextInput(attrs={'placeholder': 'Rua, número, bairro...'}),
            'telefone': forms.TextInput(attrs={'placeholder': 'Ex: (67) 99999-9999'}),
        }