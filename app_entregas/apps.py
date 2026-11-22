from django.apps import AppConfig

# Configuração padrão do Django para o app 
# O 'name' precisa ser exatamente o nome da pasta do app.
# É pelo fato de existir essa classe que o Django consegue registrar o app_entregas 
# no arquivo settings.py (na lista INSTALLED_APPS)
class AppEntregasConfig(AppConfig):
    name = 'app_entregas'