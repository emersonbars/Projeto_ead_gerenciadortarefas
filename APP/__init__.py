from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Cria a instância principal da aplicação
app = Flask(__name__)
# Carrega as configurações a partir do arquivo config.py
app.config.from_object(Config)

# Cria as instâncias das extensões
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Configuração extra para o Flask-Login
# 'login_view' diz ao Flask-Login qual é a rota da página de login.
# Se um usuário não logado tentar acessar uma página protegida,
# ele será redirecionado para '/login'.
login_manager.login_view = 'login'
# 'login_message' é a mensagem que será exibida para o usuário.
login_manager.login_message_category = 'info' # Categoria para estilização (opcional)


# A importação de rotas e modelos deve vir DEPOIS da criação de 'app' e 'db'
# para evitar erros de importação circular.
from APP import routes, models
