from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.reserva import Reserva

reserva_bp = Blueprint('reserva', __name__)

@reserva_bp.route('/reservas')
def listar_reservas():
   
    id_professor = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
  
    if not id_professor or tipo_usuario != 'professor':
        flash('Você precisa estar logado como professor!', 'error')
        return redirect(url_for('auth.login'))
    
    reserva_model = Reserva()
    reservas = reserva_model.listar_por_professor(id_professor)
    
    return render_template('reservas/listar.html', reservas=reservas)

@reserva_bp.route('/reservas/nova', methods=['GET'])
def form_nova_reserva():
    
    id_professor = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if not id_professor or tipo_usuario != 'professor':
        flash('Você precisa estar logado como professor!', 'error')
        return redirect(url_for('auth.login'))
    
    reserva_model = Reserva()
    salas = reserva_model.listar_salas_disponiveis()
    equipamentos = reserva_model.listar_equipamentos_disponiveis()
    
    return render_template('reservas/nova.html', salas=salas, equipamentos=equipamentos)

@reserva_bp.route('/reservas/nova', methods=['POST'])
def criar_reserva():
 
    tipo = request.form['tipo']
    data = request.form['data']
    horario_inicio = request.form['horario_inicio']
    horario_fim = request.form['horario_fim']
    finalidade = request.form['finalidade']
    
    id_sala = request.form.get('id_sala') if tipo == 'sala' else None
    id_equipamento = request.form.get('id_equipamento') if tipo == 'equipamento' else None
    
    id_professor = session.get('usuario_id')
    
    if not id_professor:
        flash('Você precisa estar logado!', 'error')
        return redirect(url_for('auth.login'))

    reserva_model = Reserva()
    sucesso = reserva_model.criar(
        tipo=tipo,
        id_professor=id_professor,
        data=data,
        horario_inicio=horario_inicio,
        horario_fim=horario_fim,
        finalidade=finalidade,
        id_sala=id_sala,
        id_equipamento=id_equipamento
    )
    
    if sucesso:
        flash('Reserva criada com sucesso! Aguardando aprovação do administrador.', 'success')
    else:
        flash('Erro ao criar reserva! Verifique se o horário está disponível.', 'error')
    
    return redirect(url_for('reserva.listar_reservas'))

@reserva_bp.route('/reservas/<int:id>')
def ver_reserva(id):

    reserva_model = Reserva()
    reserva = reserva_model.buscar_por_id(id)
    
    if not reserva:
        flash('Reserva não encontrada!', 'error')
        return redirect(url_for('reserva.listar_reservas'))
    
  
    id_professor = session.get('usuario_id')
    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario == 'professor' and reserva['id_professor'] != id_professor:
        flash('Você não tem permissão para ver essa reserva!', 'error')
        return redirect(url_for('reserva.listar_reservas'))
    
    return render_template('reservas/detalhes.html', reserva=reserva)

@reserva_bp.route('/reservas/cancelar/<int:id>', methods=['POST'])
def cancelar_reserva(id):

    reserva_model = Reserva()
    reserva = reserva_model.buscar_por_id(id)
    
    if not reserva:
        flash('Reserva não encontrada!', 'error')
        return redirect(url_for('reserva.listar_reservas'))

    id_professor = session.get('usuario_id')
    
    if reserva['id_professor'] != id_professor:
        flash('Você só pode cancelar suas próprias reservas!', 'error')
        return redirect(url_for('reserva.listar_reservas'))
    

    sucesso = reserva_model.cancelar(id)
    
    if sucesso:
        flash('Reserva cancelada com sucesso!', 'success')
    else:
        flash('Erro ao cancelar reserva!', 'error')
    
    return redirect(url_for('reserva.listar_reservas'))

@reserva_bp.route('/admin/reservas')
def admin_listar_reservas():

    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado! Apenas administradores.', 'error')
        return redirect(url_for('reserva.listar_reservas'))
    
    reserva_model = Reserva()
    reservas = reserva_model.listar_todas()
    
    return render_template('admin/reservas/listar.html', reservas=reservas)


@reserva_bp.route('/admin/reservas/pendentes')
def admin_listar_pendentes():

    
    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado! Apenas administradores.', 'error')
        return redirect(url_for('reserva.listar_reservas'))
    
    reserva_model = Reserva()
    reservas = reserva_model.listar_pendentes()
    
    return render_template('admin/reservas/pendentes.html', reservas=reservas)


@reserva_bp.route('/admin/reservas/aprovar/<int:id>', methods=['POST'])
def admin_aprovar_reserva(id):

    
    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('reserva.listar_reservas'))
    
    reserva_model = Reserva()
    sucesso = reserva_model.aprovar(id)
    
    if sucesso:
        flash('Reserva aprovada com sucesso!', 'success')
    else:
        flash('Erro ao aprovar reserva!', 'error')
    
    return redirect(url_for('reserva.admin_listar_pendentes'))


@reserva_bp.route('/admin/reservas/reprovar/<int:id>', methods=['POST'])
def admin_reprovar_reserva(id):
    
    
    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('reserva.listar_reservas'))
    
    reserva_model = Reserva()
    sucesso = reserva_model.reprovar(id)
    
    if sucesso:
        flash('Reserva reprovada!', 'success')
    else:
        flash('Erro ao reprovar reserva!', 'error')
    
    return redirect(url_for('reserva.admin_listar_pendentes'))


@reserva_bp.route('/admin/reservas/cancelar/<int:id>', methods=['POST'])
def admin_cancelar_reserva(id):
    
    
    tipo_usuario = session.get('tipo_usuario')
    
    if tipo_usuario != 'administrador':
        flash('Acesso negado!', 'error')
        return redirect(url_for('reserva.listar_reservas'))
    
    reserva_model = Reserva()
    sucesso = reserva_model.cancelar(id)
    
    if sucesso:
        flash('Reserva cancelada com sucesso!', 'success')
    else:
        flash('Erro ao cancelar reserva!', 'error')
    
    return redirect(url_for('reserva.admin_listar_reservas'))