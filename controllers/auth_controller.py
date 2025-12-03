from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario import Usuario


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login_page():

    return render_template('auth/login.html')

@auth_bp.route('/login', methods=['POST'])
def fazer_login():
    email = request.form['email']
    senha = request.form['senha']
    tipo_usuario = request.form['tipo']     
    usuario_model = Usuario()

    if tipo_usuario == 'aluno':
        usuario = usuario_model.login_aluno(email, senha)
        tipo_sessao = 'aluno'
        redirect_url = '/aluno/dashboard'  
        
    elif tipo_usuario == 'professor':
        usuario = usuario_model.login_professor(email, senha)
        tipo_sessao = 'professor'
        redirect_url = '/professor/dashboard'
        
    elif tipo_usuario == 'admin':
        usuario = usuario_model.login_admin(email, senha)
        tipo_sessao = 'administrador'
        redirect_url = '/admin/avisos'
    else:
        flash('Tipo de usuário inválido!', 'error')
        return redirect(url_for('auth.login_page'))
    
    if usuario:
        session['usuario_id'] = usuario['id']           # ID do banco
        session['usuario_nome'] = usuario['nome']       # Nome
        session['usuario_email'] = usuario['email']     # Email
        session['usuario_tipo'] = tipo_sessao          # Tipo (aluno/professor/admin)
        
        flash(f'Bem-vindo(a), {usuario["nome"]}!', 'success')
        return redirect(redirect_url)
    
    else:
        flash('Email ou senha incorretos!', 'error')
        return redirect(url_for('auth.login_page'))

@auth_bp.route('/logout')
def logout():
    
    nome = session.get('usuario_nome', 'Usuário')
    session.clear()
    flash(f'Até logo, {nome}!', 'success')
    
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/registro/aluno', methods=['GET'])
def registro_aluno_page():
    return render_template('auth/registro_aluno.html')

@auth_bp.route('/registro/aluno', methods=['POST'])
def registrar_aluno():

    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']
    
    if senha != confirmar_senha:
        flash('As senhas não coincidem!', 'error')
        return redirect(url_for('auth.registro_aluno_page'))
    
    if len(senha) < 6:
        flash('A senha deve ter no mínimo 6 caracteres!', 'error')
        return redirect(url_for('auth.registro_aluno_page'))
    
    usuario_model = Usuario()
    sucesso = usuario_model.registrar_aluno(nome, email, senha)
    
    if sucesso:
        flash('Aluno registrado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login_page'))
    else:
        flash('Email já cadastrado ou erro ao registrar!', 'error')
        return redirect(url_for('auth.registro_aluno_page'))

@auth_bp.route('/registro/professor', methods=['GET'])
def registro_professor_page():
    return render_template('auth/registro_professor.html')

@auth_bp.route('/registro/professor', methods=['POST'])
def registrar_professor():
    nome = request.form['nome']
    email = request.form['email']
    especialidade = request.form['especialidade']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']

    if senha != confirmar_senha:
        flash('As senhas não coincidem!', 'error')
        return redirect(url_for('auth.registro_professor_page'))
    
    if len(senha) < 6:
        flash('A senha deve ter no mínimo 6 caracteres!', 'error')
        return redirect(url_for('auth.registro_professor_page'))

    usuario_model = Usuario()
    sucesso = usuario_model.registrar_professor(nome, email, especialidade, senha)
    
    if sucesso:
        flash('Professor registrado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login_page'))
    else:
        flash('Email já cadastrado ou erro ao registrar!', 'error')
        return redirect(url_for('auth.registro_professor_page'))

@auth_bp.route('/registro/admin', methods=['GET'])
def registro_admin_page():
    return render_template('auth/registro_admin.html')

@auth_bp.route('/registro/admin', methods=['POST'])
def registrar_admin():

    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']
    senha_mestra = request.form['senha_mestra']  # Senha especial para criar admin
    
    if senha != confirmar_senha:
        flash('As senhas não coincidem!', 'error')
        return redirect(url_for('auth.registro_admin_page'))
    
    if len(senha) < 6:
        flash('A senha deve ter no mínimo 6 caracteres!', 'error')
        return redirect(url_for('auth.registro_admin_page'))
    
    usuario_model = Usuario()
    sucesso = usuario_model.registrar_admin(nome, email, senha, senha_mestra)
    
    if sucesso:
        flash('Administrador registrado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login_page'))
    else:
        flash('Senha mestra incorreta, email já cadastrado ou erro!', 'error')
        return redirect(url_for('auth.registro_admin_page'))