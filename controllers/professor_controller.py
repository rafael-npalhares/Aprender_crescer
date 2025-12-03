from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.professor import Professor

professor_bp = Blueprint('professor', __name__)


@professor_bp.route('/professor/perfil')
def perfil():
    id_professor = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_professor or tipo_usuario != 'professor':
        flash('Você precisa estar logado como professor!', 'error')
        return redirect(url_for('auth.form_login'))
    
    professor_model = Professor()
    professor = professor_model.buscar_meus_detalhes_completos(id_professor)
    
    if not professor:
        flash('Professor não encontrado!', 'error')
        return redirect(url_for('index'))
    
    return render_template('professor/perfil.html', professor=professor)


@professor_bp.route('/professor/perfil/editar', methods=['GET'])
def form_editar_perfil():
    id_professor = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_professor or tipo_usuario != 'professor':
        flash('Você precisa estar logado como professor!', 'error')
        return redirect(url_for('auth.form_login'))
    
    professor_model = Professor()
    professor = professor_model.buscar_por_id(id_professor)
    
    return render_template('professor/editar_perfil.html', professor=professor)


@professor_bp.route('/professor/perfil/editar', methods=['POST'])
def editar_perfil():
    id_professor = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_professor or tipo_usuario != 'professor':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.form_login'))
    
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    especialidade = request.form.get('especialidade', '').strip()
    
    if not nome or not email or not especialidade:
        flash('Preencha todos os campos!', 'error')
        return redirect(url_for('professor.form_editar_perfil'))
    
    if '@' not in email or '.' not in email:
        flash('Digite um email válido!', 'error')
        return redirect(url_for('professor.form_editar_perfil'))
    
    professor_model = Professor()
    sucesso = professor_model.atualizar_meu_perfil(id_professor, nome, email, especialidade)
    
    if sucesso:
        session['nome_usuario'] = nome
        flash('Perfil atualizado com sucesso!', 'success')
    else:
        flash('Erro ao atualizar perfil!', 'error')
    
    return redirect(url_for('professor.perfil'))


@professor_bp.route('/professor/horarios')
def meus_horarios():
    id_professor = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_professor or tipo_usuario != 'professor':
        flash('Você precisa estar logado como professor!', 'error')
        return redirect(url_for('auth.form_login'))
    
    professor_model = Professor()
    horarios = professor_model.buscar_meus_horarios(id_professor)
    horarios_organizados = professor_model.organizar_horarios_por_dia(horarios)
    
    return render_template('professor/horarios.html', horarios_organizados=horarios_organizados)


@professor_bp.route('/professor/turmas')
def minhas_turmas():
    id_professor = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_professor or tipo_usuario != 'professor':
        flash('Você precisa estar logado como professor!', 'error')
        return redirect(url_for('auth.form_login'))
    
    professor_model = Professor()
    turmas = professor_model.buscar_minhas_turmas(id_professor)
    
    return render_template('professor/turmas.html', turmas=turmas)


@professor_bp.route('/professor/disciplinas')
def minhas_disciplinas():
    id_professor = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_professor or tipo_usuario != 'professor':
        flash('Você precisa estar logado como professor!', 'error')
        return redirect(url_for('auth.form_login'))
    
    professor_model = Professor()
    disciplinas = professor_model.buscar_minhas_disciplinas(id_professor)
    
    return render_template('professor/disciplinas.html', disciplinas=disciplinas)