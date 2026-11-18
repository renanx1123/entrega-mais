# 🚚 Entrega+ | Sistema de Gerenciamento de Entregas

Sistema web beta para centralizar solicitações de entrega, conectar lojas e organizar o trabalho de entregadores.

## 🛠 Tecnologias
- Python 3
- Django 6
- HTML / CSS
- Banco de Dados: SQLite (Desenvolvimento) e PostgreSQL (Produção)

## 🚀 Funcionalidades
- Cadastro e Autenticação de usuários
- Lojas podem cadastrar pedidos e agrupar em rotas
- Entregadores podem aceitar rotas, coletar e entregar pedidos
- Histórico completo para Lojas e Entregadores
- Painel administrativo

## 🌐 Deploy
O sistema está online e pode ser acessado em: [entrega-mais.onrender.com](https://entrega-mais.onrender.com)

## 💻 Como rodar o projeto localmente
```bash
# Clone o repositório
git clone https://github.com/renanx1123/entrega-mais.git
cd entrega-mais

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/Scripts/activate # (Windows)

# Instale as dependências
pip install -r requirements.txt

# Rode as migrações e inicie o servidor
python manage.py migrate
python manage.py runserver
