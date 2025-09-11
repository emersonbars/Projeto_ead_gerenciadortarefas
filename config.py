import os

class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'

    
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:270894@localhost/gerenciador_tarefas'
    
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
