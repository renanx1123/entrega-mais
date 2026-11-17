from django.contrib import admin
from .models import Loja, Entregador, Rota, Entrega

admin.site.register(Loja)
admin.site.register(Entregador)
admin.site.register(Rota)
admin.site.register(Entrega)