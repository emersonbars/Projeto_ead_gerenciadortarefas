from APP import db, login_manager
from flask_login import UserMixin

# A função 'load_user' é necessária para o Flask-Login.
# Ela diz como encontrar um usuário a partir de um ID que está na sessão.
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# A nossa classe Usuario herda de db.Model (para ser um modelo do SQLAlchemy)
# e de UserMixin (para ter as funcionalidades padrão do Flask-Login).
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario' # Define o nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'

