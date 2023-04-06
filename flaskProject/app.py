from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///continental.db'
db = SQLAlchemy(app)


class Funcionario(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(length=256), nullable=False)
    email = db.Column(db.String(length=256), nullable=False, unique=True)
    password = db.Column(db.String(length=30), nullable=False)
    posto = db.Column(db.Integer(), nullable=False)
    linha = db.Column(db.Integer(), nullable=False)
    id_turno = db.Column(db.Integer(), db.ForeignKey('turno.id'), nullable=False)
    turno = db.relationship('Turno', backref='funcionarios')

class Turno(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inicio_turno = db.Column(db.DateTime(), nullable=False)
    fim_turno = db.Column(db.DateTime(), nullable=False)


with app.app_context():
    db.create_all()

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


@app.route('/paginasupervisores')
def pagina_supervisores():
    return render_template('PagGeralSupervisores.html')


if __name__ == '__main__':
    app.run()