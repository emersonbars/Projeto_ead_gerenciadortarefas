# 1. IMPORTAÇÃO ADICIONADA
from datetime import datetime
from flask import render_template, redirect, url_for, request, flash
from APP import app, db, bcrypt
from APP.models import Usuario, Tarefa
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


        if not username or not email or not password:
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('cadastro'))

        senha_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        novo_usuario = Usuario(username=username, email=email, password_hash=senha_hash)

        db.session.add(novo_usuario)
        db.session.commit()

        flash('Sua conta foi criada com sucesso! Você já pode fazer login.', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
   
    if request.method == 'POST':
        titulo_tarefa = request.form.get('titulo')
        data_prazo_str = request.form.get('data_prazo')
        hora_prazo_str = request.form.get('hora_prazo')
        
       
        print(f"--- DEBUG: Recebido do formulário: Título='{titulo_tarefa}', Data='{data_prazo_str}', Hora='{hora_prazo_str}' ---")
        
        if titulo_tarefa and data_prazo_str and hora_prazo_str:
            
            print("--- DEBUG: Todos os campos foram preenchidos. Tentando processar... ---")
            
            try:
                prazo_str_completo = f"{data_prazo_str} {hora_prazo_str}"
                prazo_obj = datetime.strptime(prazo_str_completo, '%Y-%m-%d %H:%M')
                
                
                print(f"--- DEBUG: Objeto datetime criado com sucesso: {prazo_obj} ---")

                nova_tarefa = Tarefa(
                    titulo=titulo_tarefa, 
                    data_prazo=prazo_obj,
                    usuario_id=current_user.id
                )
                
                db.session.add(nova_tarefa)
                db.session.commit()
                flash('Tarefa adicionada com sucesso!', 'success')
                print("--- DEBUG: Tarefa salva no banco de dados com sucesso! ---")

            except Exception as e:
                
                print(f"--- ERRO: Ocorreu uma exceção: {e} ---")
                flash('Ocorreu um erro ao processar a data e a hora.', 'danger')

        else:
            
            print("--- DEBUG: Um ou mais campos estavam vazios. Caindo no 'else'. ---")
            flash('Por favor, preencha todos os campos: título, data e hora.', 'danger')
        
        return redirect(url_for('dashboard'))

    tarefas_do_usuario = Tarefa.query.filter_by(usuario_id=current_user.id).order_by(Tarefa.data_criacao.desc()).all()
    return render_template('dashboard.html', tarefas=tarefas_do_usuario)

@app.route('/logout')
@login_required 
def logout():
    logout_user() 
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))
