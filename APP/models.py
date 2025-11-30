from APP import db, login_manager
from flask_login import UserMixin
from datetime import datetime, date

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario' 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    data_prazo = db.Column(db.DateTime, nullable=True) 

    concluida = db.Column(db.Boolean, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)


    @property
    def status_prazo(self):
        if self.concluida:
            return 'concluida'
            
        if self.data_prazo is None:
            return 'sem_prazo'
        

        hoje = datetime.now().date()
        prazo_data = self.data_prazo.date()

        if prazo_data < hoje:
            return 'atrasada'
        elif prazo_data == hoje:
            return 'hoje'
        else:
            return 'pendente'
    def __repr__(self):
        return f"Tarefa('{self.titulo}', '{self.data_criacao}')"
