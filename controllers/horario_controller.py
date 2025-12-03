
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.horario import Horario
from models.turma import Turma
from models.disciplina import Disciplina
from models.aluno import Aluno

horario_bp = Blueprint('horario', __name__)

@horario_bp.route('/horarios')
def listar_horarios():

    tipo_usuario = session.get('usuario_tipo')
    
    if tipo_usuario == 'aluno':
        return redirect(url_for('horario.horarios_aluno'))
    elif tipo_usuario == 'professor':
        return redirect(url_for('horario.horarios_professor'))
    elif tipo_usuario == 'administrador':
        return redirect(url_for('horario.admin_listar_turmas'))
    else:
        flash('Você precisa estar logado!', 'error')
        return redirect(url_for('auth.login_page'))


@horario_bp.route('/aluno/horarios')
def horarios_aluno():

    if session.get('usuario_tipo') != 'aluno':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    id_aluno = session.get('usuario_id')
    
    aluno_model = Aluno()
    turma = aluno_model.buscar_turma(id_aluno)
    
    if not turma:
        flash('Você ainda não está matriculado em nenhuma turma.', 'info')
        return render_template('aluno/horarios.html', 
                             turma=None, 
                             horarios=[])
    
    horario_model = Horario()
    horarios = horario_model.listar_por_turma(turma['id'])
    
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
    
    return render_template('aluno/horarios.html', 
                         turma=turma,
                         horarios=horarios,
                         horarios_organizados=horarios_organizados)


@horario_bp.route('/professor/horarios')
def horarios_professor():

    if session.get('usuario_tipo') != 'professor':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    id_professor = session.get('usuario_id')
    
    horario_model = Horario()
    horarios = horario_model.listar_por_professor(id_professor)
    

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
    
    return render_template('professor/horarios.html',
                         horarios=horarios,
                         horarios_organizados=horarios_organizados)

@horario_bp.route('/admin/horarios')
def admin_listar_turmas():

    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    turma_model = Turma()
    turmas = turma_model.listar_ativas()
    
    return render_template('admin/horarios/listar_turmas.html', 
                         turmas=turmas)


@horario_bp.route('/admin/horarios/turma/<int:id_turma>')
def admin_horarios_turma(id_turma):

    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    turma_model = Turma()
    turma = turma_model.buscar_por_id(id_turma)
    
    if not turma:
        flash('Turma não encontrada!', 'error')
        return redirect(url_for('horario.admin_listar_turmas'))
    
    horario_model = Horario()
    horarios = horario_model.listar_por_turma(id_turma)
    

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
    
    return render_template('admin/horarios/gerenciar.html',
                         turma=turma,
                         horarios=horarios,
                         horarios_organizados=horarios_organizados)


@horario_bp.route('/admin/horarios/criar', methods=['GET'])
def admin_form_criar_horario():

    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))

    id_turma = request.args.get('turma')
    
    if not id_turma:
        flash('Turma não especificada!', 'error')
        return redirect(url_for('horario.admin_listar_turmas'))
    
    turma_model = Turma()
    turma = turma_model.buscar_por_id(id_turma)
    
    if not turma:
        flash('Turma não encontrada!', 'error')
        return redirect(url_for('horario.admin_listar_turmas'))
    

    disciplina_model = Disciplina()
    disciplinas = disciplina_model.listar_todas()
    professores = []  
    salas = [] 
    return render_template('admin/horarios/criar.html',
                         turma=turma,
                         disciplinas=disciplinas,
                         professores=professores,
                         salas=salas)


@horario_bp.route('/admin/horarios/criar', methods=['POST'])
def admin_criar_horario():
 
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    id_turma = request.form['id_turma']
    dia_semana = request.form['dia_semana']
    horario_inicio = request.form['horario_inicio']
    horario_fim = request.form['horario_fim']
    id_professor = request.form['id_professor']
    id_disciplina = request.form['id_disciplina']
    id_sala = request.form.get('id_sala') or None
    
    if horario_inicio >= horario_fim:
        flash('Horário de início deve ser antes do horário de fim!', 'error')
        return redirect(url_for('horario.admin_form_criar_horario', turma=id_turma))
    
    horario_model = Horario()
    sucesso, mensagem = horario_model.criar(
        id_turma, dia_semana, horario_inicio, horario_fim,
        id_professor, id_disciplina, id_sala
    )
    
    if sucesso:
        flash(mensagem, 'success')
    else:
        flash(mensagem, 'error')
    
    return redirect(url_for('horario.admin_horarios_turma', id_turma=id_turma))


@horario_bp.route('/admin/horarios/editar/<int:id>', methods=['GET'])
def admin_form_editar_horario(id):
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    horario_model = Horario()
    horario = horario_model.buscar_por_id(id)
    
    if not horario:
        flash('Horário não encontrado!', 'error')
        return redirect(url_for('horario.admin_listar_turmas'))
    
    turma_model = Turma()
    turma = turma_model.buscar_por_id(horario['id_turma'])
    
    disciplina_model = Disciplina()
    disciplinas = disciplina_model.listar_todas()
    
    professores = []
    salas = []
    
    return render_template('admin/horarios/editar.html',
                         horario=horario,
                         turma=turma,
                         disciplinas=disciplinas,
                         professores=professores,
                         salas=salas)


@horario_bp.route('/admin/horarios/editar/<int:id>', methods=['POST'])
def admin_editar_horario(id):
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    id_turma = request.form['id_turma']
    dia_semana = request.form['dia_semana']
    horario_inicio = request.form['horario_inicio']
    horario_fim = request.form['horario_fim']
    id_professor = request.form['id_professor']
    id_disciplina = request.form['id_disciplina']
    id_sala = request.form.get('id_sala') or None
    
    if horario_inicio >= horario_fim:
        flash('Horário de início deve ser antes do horário de fim!', 'error')
        return redirect(url_for('horario.admin_form_editar_horario', id=id))
    
    horario_model = Horario()
    sucesso, mensagem = horario_model.editar(
        id, id_turma, dia_semana, horario_inicio, horario_fim,
        id_professor, id_disciplina, id_sala
    )
    
    if sucesso:
        flash(mensagem, 'success')
    else:
        flash(mensagem, 'error')
    
    return redirect(url_for('horario.admin_horarios_turma', id_turma=id_turma))


@horario_bp.route('/admin/horarios/deletar/<int:id>', methods=['POST'])
def admin_deletar_horario(id):
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    horario_model = Horario()
    horario = horario_model.buscar_por_id(id)
    if not horario:
        flash('Horário não encontrado!', 'error')
        return redirect(url_for('horario.admin_listar_turmas'))
    id_turma = horario['id_turma']
    sucesso = horario_model.deletar(id)
    if sucesso:
        flash('Horário deletado com sucesso!', 'success')
    else:
        flash('Erro ao deletar horário!', 'error')
    
    return redirect(url_for('horario.admin_horarios_turma', id_turma=id_turma))

@horario_bp.route('/admin/turmas')
def admin_gerenciar_turmas():
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    turma_model = Turma()
    turmas = turma_model.listar_todas()
    
    return render_template('admin/turmas/listar.html', turmas=turmas)


@horario_bp.route('/admin/turmas/criar', methods=['POST'])
def admin_criar_turma():
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    nome = request.form['nome']
    
    turma_model = Turma()
    sucesso = turma_model.criar(nome)
    
    if sucesso:
        flash('Turma criada com sucesso!', 'success')
    else:
        flash('Erro ao criar turma! Nome já existe.', 'error')
    
    return redirect(url_for('horario.admin_gerenciar_turmas'))


@horario_bp.route('/admin/turmas/editar/<int:id>', methods=['POST'])
def admin_editar_turma(id):
    """Admin: Edita nome da turma"""
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    nome = request.form['nome']
    
    turma_model = Turma()
    sucesso = turma_model.atualizar(id, nome)
    
    if sucesso:
        flash('Turma atualizada com sucesso!', 'success')
    else:
        flash('Erro ao atualizar turma!', 'error')
    
    return redirect(url_for('horario.admin_gerenciar_turmas'))


@horario_bp.route('/admin/turmas/desativar/<int:id>', methods=['POST'])
def admin_desativar_turma(id):
    """Admin: Desativa uma turma"""
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    turma_model = Turma()
    sucesso = turma_model.desativar(id)
    
    if sucesso:
        flash('Turma desativada!', 'success')
    else:
        flash('Erro ao desativar turma!', 'error')
    
    return redirect(url_for('horario.admin_gerenciar_turmas'))


@horario_bp.route('/admin/turmas/ativar/<int:id>', methods=['POST'])
def admin_ativar_turma(id):
    """Admin: Ativa uma turma"""
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    turma_model = Turma()
    sucesso = turma_model.ativar(id)
    
    if sucesso:
        flash('Turma ativada!', 'success')
    else:
        flash('Erro ao ativar turma!', 'error')
    
    return redirect(url_for('horario.admin_gerenciar_turmas'))


@horario_bp.route('/admin/turmas/deletar/<int:id>', methods=['POST'])
def admin_deletar_turma(id):
    """Admin: Deleta uma turma"""
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    turma_model = Turma()
    sucesso = turma_model.deletar(id)
    
    if sucesso:
        flash('Turma deletada com sucesso!', 'success')
    else:
        flash('Erro ao deletar turma!', 'error')
    
    return redirect(url_for('horario.admin_gerenciar_turmas'))

@horario_bp.route('/admin/disciplinas')
def admin_gerenciar_disciplinas():
    """Admin: Gerenciar disciplinas (CRUD)"""
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    disciplina_model = Disciplina()
    disciplinas = disciplina_model.listar_todas()
    
    return render_template('admin/disciplinas/listar.html', 
                         disciplinas=disciplinas)


@horario_bp.route('/admin/disciplinas/criar', methods=['POST'])
def admin_criar_disciplina():
    """Admin: Cria nova disciplina"""
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    nome = request.form['nome']
    
    disciplina_model = Disciplina()
    sucesso = disciplina_model.criar(nome)
    
    if sucesso:
        flash('Disciplina criada com sucesso!', 'success')
    else:
        flash('Erro! Disciplina já existe.', 'error')
    
    return redirect(url_for('horario.admin_gerenciar_disciplinas'))


@horario_bp.route('/admin/disciplinas/editar/<int:id>', methods=['POST'])
def admin_editar_disciplina(id):
    """Admin: Edita disciplina"""
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    nome = request.form['nome']
    
    disciplina_model = Disciplina()
    sucesso = disciplina_model.atualizar(id, nome)
    
    if sucesso:
        flash('Disciplina atualizada!', 'success')
    else:
        flash('Erro ao atualizar!', 'error')
    
    return redirect(url_for('horario.admin_gerenciar_disciplinas'))


@horario_bp.route('/admin/disciplinas/deletar/<int:id>', methods=['POST'])
def admin_deletar_disciplina(id):
    """Admin: Deleta disciplina"""
    if session.get('usuario_tipo') != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('auth.login_page'))
    
    disciplina_model = Disciplina()
    sucesso = disciplina_model.deletar(id)
    
    if sucesso:
        flash('Disciplina deletada!', 'success')
    else:
        flash('Erro ao deletar!', 'error')
    
    return redirect(url_for('horario.admin_gerenciar_disciplinas'))