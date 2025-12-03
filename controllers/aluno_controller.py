
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.aluno import Aluno

aluno_bp = Blueprint('aluno', __name__)

@aluno_bp.route('/aluno/perfil')
def perfil():

    id_aluno = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_aluno or tipo_usuario != 'aluno':
        flash('Você precisa estar logado como aluno!', 'error')
        return redirect(url_for('auth.form_login'))
    
    aluno_model = Aluno()
    aluno = aluno_model.buscar_por_id(id_aluno)
    turma = aluno_model.buscar_turma(id_aluno)
    
    if not aluno:
        flash('Aluno não encontrado!', 'error')
        return redirect(url_for('index'))
    
    return render_template('aluno/perfil.html', aluno=aluno, turma=turma)

@aluno_bp.route('/aluno/perfil/editar', methods=['GET'])
def form_editar_perfil():

    id_aluno = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_aluno or tipo_usuario != 'aluno':
        flash('Você precisa estar logado como aluno!', 'error')
        return redirect(url_for('auth.form_login'))
    
    aluno_model = Aluno()
    aluno = aluno_model.buscar_por_id(id_aluno)
    
    return render_template('aluno/editar_perfil.html', aluno=aluno)

@aluno_bp.route('/aluno/perfil/editar', methods=['POST'])
def editar_perfil():
 
    id_aluno = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_aluno or tipo_usuario != 'aluno':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.form_login'))
    
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    
    if not nome or not email:
        flash('Preencha todos os campos!', 'error')
        return redirect(url_for('aluno.form_editar_perfil'))
    
    if '@' not in email or '.' not in email:
        flash('Digite um email válido!', 'error')
        return redirect(url_for('aluno.form_editar_perfil'))

    aluno_model = Aluno()
    sucesso = aluno_model.atualizar_perfil(id_aluno, nome, email)
    
    if sucesso:

        session['nome_usuario'] = nome
        flash('Perfil atualizado com sucesso!', 'success')
    else:
        flash('Erro ao atualizar perfil!', 'error')
    
    return redirect(url_for('aluno.perfil'))

@aluno_bp.route('/aluno/horarios')
def meus_horarios():

    id_aluno = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_aluno or tipo_usuario != 'aluno':
        flash('Você precisa estar logado como aluno!', 'error')
        return redirect(url_for('auth.form_login'))
    
    aluno_model = Aluno()
    turma = aluno_model.buscar_turma(id_aluno)
    horarios = aluno_model.buscar_horarios(id_aluno)

    horarios_organizados = {
        'segunda': [],
        'terca': [],
        'quarta': [],
        'quinta': [],
        'sexta': [],
        'sabado': []
    }
    
    for horario in horarios:
        dia = horario['dia_semana']
        if dia in horarios_organizados:
            horarios_organizados[dia].append(horario)
    
    return render_template(
        'aluno/horarios.html', 
        turma=turma, 
        horarios_organizados=horarios_organizados
    )

@aluno_bp.route('/aluno/turma')
def minha_turma():

    id_aluno = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_aluno or tipo_usuario != 'aluno':
        flash('Você precisa estar logado como aluno!', 'error')
        return redirect(url_for('auth.form_login'))
    
    aluno_model = Aluno()
    turma = aluno_model.buscar_turma(id_aluno)
    
    if not turma:
        flash('Você não está vinculado a nenhuma turma!', 'error')
        return redirect(url_for('aluno.perfil'))
    
    colegas = aluno_model.listar_por_turma(turma['id'])
    
    colegas = [c for c in colegas if c['id'] != id_aluno]
    
    return render_template('aluno/turma.html', turma=turma, colegas=colegas)

@aluno_bp.route('/admin/alunos')
def admin_listar_alunos():

    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado! Apenas administradores.', 'error')
        return redirect(url_for('index'))
    
    aluno_model = Aluno()
    alunos = aluno_model.listar_todos()
    
    return render_template('admin/alunos/listar.html', alunos=alunos)

@aluno_bp.route('/admin/alunos/<int:id>')
def admin_ver_aluno(id):

    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('index'))
    
    aluno_model = Aluno()
    aluno = aluno_model.buscar_por_id(id)
    turma = aluno_model.buscar_turma(id)
    
    if not aluno:
        flash('Aluno não encontrado!', 'error')
        return redirect(url_for('aluno.admin_listar_alunos'))
    
    return render_template('admin/alunos/detalhes.html', aluno=aluno, turma=turma)

@aluno_bp.route('/admin/alunos/<int:id>/editar', methods=['GET'])
def admin_form_editar_aluno(id):

    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('index'))
    
    aluno_model = Aluno()
    aluno = aluno_model.buscar_por_id(id)
    
    if not aluno:
        flash('Aluno não encontrado!', 'error')
        return redirect(url_for('aluno.admin_listar_alunos'))
    
    return render_template('admin/alunos/editar.html', aluno=aluno)

@aluno_bp.route('/admin/alunos/<int:id>/editar', methods=['POST'])
def admin_editar_aluno(id):

    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('index'))
    
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    
    if not nome or not email:
        flash('Preencha todos os campos!', 'error')
        return redirect(url_for('aluno.admin_form_editar_aluno', id=id))
    
    aluno_model = Aluno()
    sucesso = aluno_model.atualizar_perfil(id, nome, email)
    
    if sucesso:
        flash('Aluno atualizado com sucesso!', 'success')
    else:
        flash('Erro ao atualizar aluno!', 'error')
    
    return redirect(url_for('aluno.admin_ver_aluno', id=id))

@aluno_bp.route('/admin/alunos/<int:id>/vincular-turma', methods=['GET'])
def admin_form_vincular_turma(id):
    
    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('index'))
    
    aluno_model = Aluno()
    aluno = aluno_model.buscar_por_id(id)
    
    if not aluno:
        flash('Aluno não encontrado!', 'error')
        return redirect(url_for('aluno.admin_listar_alunos'))
    
    from models.turma import Turma
    turma_model = Turma()
    turmas = turma_model.listar_ativas()
    
    turma_atual = aluno_model.buscar_turma(id)
    
    return render_template(
        'admin/alunos/vincular_turma.html', 
        aluno=aluno, 
        turmas=turmas,
        turma_atual=turma_atual
    )

@aluno_bp.route('/admin/alunos/<int:id>/vincular-turma', methods=['POST'])
def admin_vincular_turma(id):

    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('index'))
    
    id_turma = request.form.get('id_turma')
    
    if not id_turma:
        flash('Selecione uma turma!', 'error')
        return redirect(url_for('aluno.admin_form_vincular_turma', id=id))
    
    aluno_model = Aluno()

    turma_atual = aluno_model.buscar_turma(id)
    if turma_atual:
        aluno_model.desvincular_turma(id, turma_atual['id'])

    sucesso = aluno_model.vincular_turma(id, id_turma)
    
    if sucesso:
        flash('Aluno vinculado à turma com sucesso!', 'success')
    else:
        flash('Erro ao vincular aluno à turma!', 'error')
    
    return redirect(url_for('aluno.admin_ver_aluno', id=id))


@aluno_bp.route('/admin/alunos/<int:id>/desvincular-turma', methods=['POST'])
def admin_desvincular_turma(id):

    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('index'))
    
    aluno_model = Aluno()
    turma_atual = aluno_model.buscar_turma(id)
    
    if not turma_atual:
        flash('Aluno não está vinculado a nenhuma turma!', 'error')
        return redirect(url_for('aluno.admin_ver_aluno', id=id))
    
    sucesso = aluno_model.desvincular_turma(id, turma_atual['id'])
    
    if sucesso:
        flash('Aluno removido da turma!', 'success')
    else:
        flash('Erro ao remover aluno da turma!', 'error')
    
    return redirect(url_for('aluno.admin_ver_aluno', id=id))


@aluno_bp.route('/admin/alunos/<int:id>/deletar', methods=['POST'])
def admin_deletar_aluno(id):

    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('index'))
    
    aluno_model = Aluno()
    sucesso = aluno_model.deletar(id)
    
    if sucesso:
        flash('Aluno deletado com sucesso!', 'success')
    else:
        flash('Erro ao deletar aluno!', 'error')
    
    return redirect(url_for('aluno.admin_listar_alunos'))