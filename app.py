# app.py
from flask import Flask
from controllers.aviso_controller import aviso_bp

# Cria a aplicação Flask
app = Flask(__name__)


app.secret_key = "aprender_crescer_13293022"


# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)