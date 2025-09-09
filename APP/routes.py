from flask import render_template, redirect, url_for
from APP import app

# Rota para a página inicial e de login
@app.route('/')
@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/dashboard')
def dashboard():

    usuario_falso = {'username': 'Visitante'}
    return render_template('dashboard.html', current_user=usuario_falso)

# Rota para o logout
@app.route('/logout')
def logout():

    return redirect(url_for('login'))
