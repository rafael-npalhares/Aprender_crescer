from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.administrador import Administrador
from models.aviso import Aviso
from models.aluno import Aluno

aviso_model = Aviso()
admin_model = Administrador()
aluno_model = Aluno()


admin_bp = Blueprint('admin', __name__) 

@admin_bp.route('/admin/dashboard')
def dashboard():
    if session.get['usuario_tipo'] != 'administrador':
        flash('Acesso negado! Área restrita a administradores.', 'error') 
        return redirect(url_for('auth.login_page'))
    
    estatisticas = admin_model.buscar_estatisticas_sistema()
    id_admin = session.get('usuario_id')
    admin = admin_model.buscar_por_id(id_admin)
    return render_template('admin/dashboard.html', estatisticas=estatisticas, admin=admin)
   
@admin_bp.route('/admin/alunos')
def listar_alunos():
    if session.get['usuario_tipo'] != 'administrador':
        flash('Acesso negado! Área restrita a administradores.', 'error') 
        return redirect(url_for('auth.login_page'))
    
    alunos = aluno_model.listar_todos()
    return render_template('admin/gerenciar_usuarios.html', alunos=alunos, tipo='aluno')    

@admin_bp.route('/admin/alunos/criar', methods=['POST'])
def criar_aluno():
    if session.get['usuario_tipo'] != 'administrador':
        flash('Acesso negado! Área restrita a administradores.', 'error') 
        return redirect(url_for('auth.login_page'))
    
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    sucesso = aluno_model.criar(nome, email, senha)
    if sucesso:
        flash('aluno criado com sucesso!', 'success')
    else: 
        flash('Erro ao criar aluno! Email já cadastrado.', 'error')
    return redirect(url_for('admin.listar_alunos'))

@admin_bp.route('/admin/alunos/editar/<int:id>', methods=['GET'])
def form_editar_aluno(id):
    if session.get['usuario_tipo'] != 'administrador':
        flash('Acesso negado! Área restrita a administradores.', 'error') 
        return redirect(url_for('auth.login_page'))
   
    aluno = aluno_model.buscar_por_id(id)
    if not aluno:
        flash('Aluno não encontrado!', 'error')
        return redirect(url_for('admin.listar_alunos'))
    
    return render_template('admin/gerenciar_usuarios.html', usuario=aluno, tipo='aluno')

@admin_bp.route('/admin/alunos/editar/<int:id>', methods=['POST'])
def editar_aluno(id):
    if session.get['usuario_tipo'] != 'administrador':
        flash('Acesso negado! Área restrita a administradores.', 'error') 
        return redirect(url_for('auth.login_page'))
    nome = request.form['nome']
    email = request.form['email']
    success = aluno_model.atualizar_perfil(id, nome, email)
    
    if success:
        flash('Aluno atualizado com sucesso!', 'success')
    else:
        flash('Erro ao atualizar aluno!', 'error')
    
    return redirect(url_for('admin.listar_alunos'))

@admin_bp.route('/admin/alunos/deletar/<int:id>', methods=['POST'])
def deletar_aluno(id):
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    sucesso = aluno_model.deletar(id)

    if sucesso:
        flash('Aluno deletado com sucesso!', 'success')
    else:
        flash('Erro ao deletar aluno!', 'error')
    
    return redirect(url_for('admin.listar_alunos'))

@admin_bp.route('/admin/professores')
def listar_professores():
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    return render_template('admin/gerenciar_usuarios.html', administradores=admins, tipo='administrador')