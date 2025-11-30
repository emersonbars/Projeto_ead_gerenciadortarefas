from datetime import datetime
from flask import render_template, redirect, url_for, request, flash
from APP import app, db, bcrypt
from APP.models import Usuario, Tarefa
from flask_login import login_user, logout_user, login_required, current_user

# ROTA DE LOGIN (E PÁGINA INICIAL)
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

# ROTA DE CADASTRO
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

# ROTA DO DASHBOARD (PÁGINA PRINCIPAL APÓS LOGIN)
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Lógica para ADICIONAR uma nova tarefa
    if request.method == 'POST':
        titulo_tarefa = request.form.get('titulo')
        data_prazo_str = request.form.get('data_prazo')
        hora_prazo_str = request.form.get('hora_prazo')
        
        if titulo_tarefa and data_prazo_str and hora_prazo_str:
            try:
                prazo_str_completo = f"{data_prazo_str} {hora_prazo_str}"
                prazo_obj = datetime.strptime(prazo_str_completo, '%Y-%m-%d %H:%M')
                nova_tarefa = Tarefa(titulo=titulo_tarefa, data_prazo=prazo_obj, usuario_id=current_user.id)
                db.session.add(nova_tarefa)
                db.session.commit()
                flash('Tarefa adicionada com sucesso!', 'success')
            except Exception as e:
                flash('Ocorreu um erro ao processar a data e a hora.', 'danger')
        else:
            flash('Por favor, preencha todos os campos: título, data e hora.', 'danger')
        
        return redirect(url_for('dashboard'))

    # Lógica para MOSTRAR as tarefas (com filtro e ordenação)
    ordenar_por = request.args.get('ordenar_por', 'recentes')
    filtro = request.args.get('filtro', 'todas')

    query = Tarefa.query.filter_by(usuario_id=current_user.id)

    if filtro == 'pendentes':
        query = query.filter_by(concluida=False)
    elif filtro == 'concluidas':
        query = query.filter_by(concluida=True)

    if ordenar_por == 'prazo':
        query = query.order_by(Tarefa.data_prazo.is_(None), Tarefa.data_prazo.asc())
    else:
        query = query.order_by(Tarefa.data_criacao.desc())

    tarefas_do_usuario = query.all()
    
    return render_template('dashboard.html', tarefas=tarefas_do_usuario, filtro_ativo=filtro, ordenacao_ativa=ordenar_por)

# ROTA PARA CONCLUIR TAREFA
@app.route('/tarefa/<int:tarefa_id>/concluir', methods=['POST'])
@login_required
def concluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    if tarefa.usuario_id != current_user.id:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('dashboard'))
    tarefa.concluida = True
    db.session.commit()
    flash('Tarefa marcada como concluída!', 'success')
    return redirect(url_for('dashboard'))

# ROTA PARA EXCLUIR TAREFA
@app.route('/tarefa/<int:tarefa_id>/excluir', methods=['POST'])
@login_required
def excluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    if tarefa.usuario_id != current_user.id:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('dashboard'))
    db.session.delete(tarefa)
    db.session.commit()
    flash('Tarefa excluída com sucesso!', 'success')
    return redirect(url_for('dashboard'))

# ROTA PARA EDITAR TAREFA (com depuração)
@app.route('/tarefa/<int:tarefa_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_tarefa(tarefa_id):
    # Busca a tarefa que será editada
    tarefa = Tarefa.query.get_or_404(tarefa_id)

    # Segurança: Garante que o usuário só pode editar suas próprias tarefas
    if tarefa.usuario_id != current_user.id:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('dashboard'))

    # Se o formulário for enviado (método POST)
    if request.method == 'POST':
        # Pega os novos dados do formulário
        novo_titulo = request.form.get('titulo')
        nova_data_str = request.form.get('data_prazo')
        nova_hora_str = request.form.get('hora_prazo')

        print(f"--- EDITAR DEBUG: Recebido do formulário: Título='{novo_titulo}', Data='{nova_data_str}', Hora='{nova_hora_str}' ---")

        if novo_titulo and nova_data_str and nova_hora_str:
            try:
                print(f"--- EDITAR DEBUG: Título antigo: {tarefa.titulo}, Prazo antigo: {tarefa.data_prazo} ---")

                # Atualiza os campos da tarefa com os novos valores
                tarefa.titulo = novo_titulo
                
                prazo_str_completo = f"{nova_data_str} {nova_hora_str}"
                tarefa.data_prazo = datetime.strptime(prazo_str_completo, '%Y-%m-%d %H:%M')

                print(f"--- EDITAR DEBUG: Título novo: {tarefa.titulo}, Prazo novo: {tarefa.data_prazo} ---")

                # Confirma a alteração no banco de dados
                print("--- EDITAR DEBUG: Tentando salvar (db.session.commit())... ---")
                db.session.commit()
                print("--- EDITAR DEBUG: Salvo com sucesso! ---")

                flash('Tarefa atualizada com sucesso!', 'success')
                return redirect(url_for('dashboard'))

            except Exception as e:
                print(f"--- EDITAR ERRO: Ocorreu uma exceção: {e} ---")
                flash('Ocorreu um erro ao atualizar a tarefa.', 'danger')
        else:
            flash('Todos os campos são obrigatórios.', 'danger')
    
    # Se for a primeira vez que a página é carregada (método GET)
    # Renderiza o template, passando a tarefa para pré-preencher o formulário
    return render_template('editar_tarefa.html', tarefa=tarefa)

# ROTA DE LOGOUT
@app.route('/logout')
@login_required 
def logout():
    logout_user() 
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))
