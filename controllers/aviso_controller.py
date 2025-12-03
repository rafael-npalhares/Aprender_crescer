from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.aviso import Aviso

aviso_bp = Blueprint('aviso', __name__)

@aviso_bp.route('/avisos')
def listar_avisos():
    aviso_model = Aviso()
    avisos = aviso_model.listar_ativos()
    
    return render_template('avisos/listar.html', avisos=avisos)


@aviso_bp.route('/avisos/<int:id>')
def ver_aviso(id):
    aviso_model = Aviso()
    aviso = aviso_model.buscar_por_id(id)
    
    if not aviso:
        flash('Aviso não encontrado!', 'error')
        return redirect(url_for('aviso.listar_avisos'))
    
    return render_template('avisos/detalhes.html', aviso=aviso)


@aviso_bp.route('/admin/avisos')
def admin_listar_avisos():
    aviso_model = Aviso()
    avisos = aviso_model.listar_todos()
    return render_template('admin/avisos/listar.html', avisos=avisos)


@aviso_bp.route('/admin/avisos/criar', methods=['GET'])
def admin_form_criar_aviso():
    return render_template('admin/avisos/criar.html')


@aviso_bp.route('/admin/avisos/criar', methods=['POST'])
def admin_criar_aviso():

    titulo = request.form['titulo']
    descricao = request.form['descricao']
    tipo = request.form['tipo']
    data_expiracao = request.form.get('data_expiracao') or None
    
    id_autor = session.get('usuario_id')
    
    if not id_autor:
        flash('Você precisa estar logado!', 'error')
        return redirect(url_for('auth.login'))
    

    aviso_model = Aviso()
    sucesso = aviso_model.criar(titulo, descricao, tipo, id_autor, data_expiracao)
    
    if sucesso:
        flash('Aviso criado com sucesso!', 'success')
    else:
        flash('Erro ao criar aviso!', 'error')
    
    return redirect(url_for('aviso.admin_listar_avisos'))


@aviso_bp.route('/admin/avisos/editar/<int:id>', methods=['GET'])
def admin_form_editar_aviso(id):
    aviso_model = Aviso()
    aviso = aviso_model.buscar_por_id(id)
    
    if not aviso:
        flash('Aviso não encontrado!', 'error')
        return redirect(url_for('aviso.admin_listar_avisos'))
    
    return render_template('admin/avisos/editar.html', aviso=aviso)


@aviso_bp.route('/admin/avisos/editar/<int:id>', methods=['POST'])
def admin_editar_aviso(id):
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    tipo = request.form['tipo']
    data_expiracao = request.form.get('data_expiracao') or None
    
    aviso_model = Aviso()
    sucesso = aviso_model.editar(id, titulo, descricao, tipo, data_expiracao)
    
    if sucesso:
        flash('Aviso editado com sucesso!', 'success')
    else:
        flash('Erro ao editar aviso!', 'error')
    
    return redirect(url_for('aviso.admin_listar_avisos'))


@aviso_bp.route('/admin/avisos/deletar/<int:id>', methods=['POST'])
def admin_deletar_aviso(id):
    aviso_model = Aviso()
    sucesso = aviso_model.deletar(id)
    
    if sucesso:
        flash('Aviso deletado com sucesso!', 'success')
    else:
        flash('Erro ao deletar aviso!', 'error')
    
    return redirect(url_for('aviso.admin_listar_avisos'))


@aviso_bp.route('/admin/avisos/fixar/<int:id>', methods=['POST'])
def admin_fixar_aviso(id):
    aviso_model = Aviso()
    sucesso = aviso_model.fixar(id)
    
    if sucesso:
        flash('Aviso fixado!', 'success')
    else:
        flash('Erro ao fixar aviso!', 'error')
    
    return redirect(url_for('aviso.admin_listar_avisos'))


@aviso_bp.route('/admin/avisos/desfixar/<int:id>', methods=['POST'])
def admin_desfixar_aviso(id):
    aviso_model = Aviso()
    sucesso = aviso_model.desfixar(id)
    
    if sucesso:
        flash('Aviso desfixado!', 'success')
    else:
        flash('Erro ao desfixar aviso!', 'error')
    
    return redirect(url_for('aviso.admin_listar_avisos'))