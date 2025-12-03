
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

