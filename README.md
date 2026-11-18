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

### 3. Popular o Banco do Render (Para a apresentação)
Como o banco de produção (no Render) está vazio, na hora de apresentar, o professor vai ver tudo zerado.
*   **O que fazer:** Entre no link do seu site no Render, faça login com o admin, e **cadastre alguns dados falsos**. Crie 2 Lojas, 2 Entregadores, 3 Pedidos e monte uma Rota. Assim, a tela do sistema não estará vazia quando você mostrar.

### 4. Requisitos "Desejáveis" (Só para falar na apresentação)
No PDF de vocês, os requisitos RF 016 a 020 (Formação automática de rotas, Integração com mapas, Cálculos de fretes e financeiro) estão marcados como **"Desejável - versão futura"**. 
Você não precisa implementar eles agora, mas na apresentação, diga: *"Esses requisitos foram mapeados para a próxima versão do software, mas a arquitetura em Django já está pronta para receber essas integrações"*.

### 5. Aviso para o Grupo
Lembra que o PDF diz que o Matheus Yuri é o Especialista em Testes? O pessoal do grupo precisa fazer os testes de caixa preta (usar o sistema e ver se ele faz o que promete). Mande o link do Render para eles brincarem um pouco!

---

**Resumo:** O código está pronto. O que falta é só "embalar" o projeto para a apresentação. Crie o README, alimente o banco online com dados de teste e ensaie o que você vai falar sobre as escolhas de arquitetura. Você está no caminho certo! 🚀🏆
