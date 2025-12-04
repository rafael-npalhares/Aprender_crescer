from flask import Flask, render_template, redirect, url_for

from controllers.auth_controller import auth_bp
from controllers.aviso_controller import aviso_bp
from controllers.admin_controller import admin_bp
from controllers.aluno_controller import aluno_bp
from controllers.professor_controller import professor_bp
from controllers.horario_controller import horario_bp
from controllers.reserva_controller import reserva_bp

app = Flask(__name__)
app.secret_key = "aprender_crescer_MNRT"


app.config['SESSION_COOKIE_SECURE'] = False 
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.register_blueprint(auth_bp)
app.register_blueprint(aviso_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(professor_bp)
app.register_blueprint(horario_bp)
app.register_blueprint(reserva_bp)

@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def access_denied(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html'), 500


@app.template_filter('data_br')
def formatar_data_br(data):

    if data:
        try:
            return data.strftime('%d/%m/%Y')
        except:
            return str(data)
    return ''

@app.template_filter('hora_br')
def formatar_hora(hora):
    if hora:
        try:

            if isinstance(hora, str):
                return hora
      
            return hora.strftime('%H:%M')
        except:
            return str(hora)
    return ''

@app.template_filter('data_hora_br')
def formatar_data_hora_br(data_hora):

    if data_hora:
        try:
            return data_hora.strftime('%d/%m/%Y às %H:%M')
        except:
            return str(data_hora)
    return ''

@app.template_filter('nome_dia')
def nome_dia_semana(dia_abreviado):

    dias = {
        'segunda': 'Segunda-feira',
        'terca': 'Terça-feira',
        'quarta': 'Quarta-feira',
        'quinta': 'Quinta-feira',
        'sexta': 'Sexta-feira',
        'sabado': 'Sábado',
        'domingo': 'Domingo'
    }
    return dias.get(dia_abreviado, dia_abreviado)

@app.context_processor
def inject_user():
 
    from flask import session
    return {
        'usuario_logado': 'usuario_id' in session,
        'usuario_nome': session.get('usuario_nome'),
        'usuario_tipo': session.get('usuario_tipo'),
        'usuario_id': session.get('usuario_id')
    }

if __name__ == '__main__':
  
    app.run(debug=True)