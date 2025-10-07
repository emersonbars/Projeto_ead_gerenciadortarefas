from flask import render_template, redirect, url_for, request, flash

from APP import app, db, bcrypt
from APP.models import Usuario,Tarefa
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')


        usuario = Usuario.query.filter_by(username=username).first()


        if usuario and bcrypt.check_password_hash(usuario.password_hash, password):

            login_user(usuario)
            flash(f'Login bem-sucedido! Bem-vindo, {usuario.username}!', 'success')

            return redirect(url_for('dashboard'))
        else:

            flash('Login falhou. Verifique o nome de usuário e a senha.', 'danger')

    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')


        senha_hash = bcrypt.generate_password_hash(password).decode('utf-8')


        novo_usuario = Usuario(username=username, email=email, password_hash=senha_hash)


        db.session.add(novo_usuario)

        db.session.commit()


        flash('Sua conta foi criada com sucesso! Você já pode fazer login.', 'success')

        return redirect(url_for('login'))


    return render_template('cadastro.html')


@app.route('/dashboard')
@login_required  
def dashboard():

    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    logout_user() 
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST']) 
@login_required
def dashboard():

    if request.method == 'POST':
        titulo_tarefa = request.form.get('titulo')
        
        
        nova_tarefa = Tarefa(titulo=titulo_tarefa, autor=current_user)
        
        db.session.add(nova_tarefa)
        db.session.commit()
        
        flash('Tarefa adicionada com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    
    return render_template('dashboard.html')