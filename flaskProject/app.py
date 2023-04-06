from flask import Flask, render_template

db = SQLAlchemy()
DB_NAME = "continental.db"

app = Flask(__name__)


@app.route('/')
@app.route('/login')
def pag_inicial():
    return render_template('PagInicial.html')


@app.route('/geral')
def login_geral():
    return render_template('LoginGeral.html')


@app.route('/supervisores')
def login_supervisores():
    return render_template('LoginSupervisores.html')

if __name__ == '__main__':
    app.run()

@app.route('/paginasupervisores')
def pagina_supervisores():
    return render_template('PagGeralSupervisores.html')

