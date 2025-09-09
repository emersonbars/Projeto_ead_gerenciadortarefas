from flask import Flask


app = Flask(__name__)


app.config['SECRET_KEY'] = 'uma-chave-secreta-temporaria'


from APP import routes
