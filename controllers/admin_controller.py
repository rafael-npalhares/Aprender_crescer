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
    
    


    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/administradores')
def listar_administradores():
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    admins = admin_model.listar_todos()
    return render_template('admin/gerenciar_usuarios.html', administradores=admins, tipo='administrador')

@admin_bp.route('/admin/administradores/deletar/<int:id>', methods=['POST'])
def deletar_admin(id):
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    if id == session.get('usuario_id'):
        flash('Você não pode deletar sua própria conta!', 'error')
        return redirect(url_for('admin.listar_administradores'))
    success = admin_model.deletar(id)

    if success:
        flash('Adm deletado com sucesso!', 'success')
    else:
        flash('Não foi possível deletar adm.', 'error')
    return redirect(url_for('admin.listar_administradores'))

@admin_bp.route('/admin/perfil')
def perfil():
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    id_admin = session.get('usuario_id')
    admin_model = Administrador()
    admin = admin_model.buscar_por_id(id_admin)
    return render_template('admin/perfil.html', admin=admin)

@admin_bp.route('/admin/perfil/editar', methods=['POST'])
def editar_perfil():
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    id_admin = session.get('usuario_id')
    nome = request.form['nome']
    email = request.form['email']
    sucesso = admin_model.atualizar_perfil(id_admin, nome, email)
    
    if sucesso:
        session['usuario_nome'] = nome
        flash('Perfil atualizado com sucesso!', 'success')
    else:
        flash('Erro ao atualizar perfil! Email já em uso.', 'error')
    return redirect(url_for('admin.perfil'))

@admin_bp.route('/admin/perfil/senha', methods=['POST'])
def alterar_senha():
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    id_admin = session.get('usuario_id')
    senha_atual = request.form['senha_atual']
    nova_senha = request.form['nova_senha']
    confirmar_senha = request.form['confirmar_senha']
    
    if nova_senha != confirmar_senha:
        flash('As senhas não coincidem!', 'error')
        return redirect(url_for('admin.perfil'))
    
    if len(nova_senha) < 6:
        flash('A senha deve ter no mínimo 6 caracteres!', 'error')
        return redirect(url_for('admin.perfil'))
    sucesso = admin_model.atualizar_senha(id_admin, senha_atual, nova_senha)
    if sucesso:
        flash('Senha alterada com sucesso!', 'success')
    else:
        flash('Senha atual incorreta!', 'error')
    
    return redirect(url_for('admin.perfil'))