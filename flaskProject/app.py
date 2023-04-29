from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///continental.db'
db = SQLAlchemy(app)


class Funcionario(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(length=256), nullable=False)
    email = db.Column(db.String(length=256), nullable=True, unique=True)
    password = db.Column(db.String(length=30), nullable=False)
    id_posto = db.Column(db.Integer(), db.ForeignKey('posto.id'), nullable=False)
    posto = db.relationship('Posto', backref='funcionarios')
    id_linha = db.Column(db.Integer(), db.ForeignKey('linha.id'), nullable=False)
    linha = db.relationship('Linha', backref='funcionarios')
    id_turno = db.Column(db.Integer(), db.ForeignKey('turno.id'), nullable=False)
    turno = db.relationship('Turno', backref='funcionarios')
    id_cargo = db.Column(db.Integer(), db.ForeignKey('cargo.id'), nullable=False)
    cargo = db.relationship('Cargo', backref='funcionarios')


class Cargo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    descricao_cargo = db.Column(db.String(length=100), nullable=False, unique=True)


class Checklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ckl_inicio = db.Column(db.DateTime(), nullable=False)
    ckl_fim = db.Column(db.DateTime(), nullable=False)
    aprovacao = db.Column(db.Boolean(), nullable=False)
    em_andamento = db.Column(db.Boolean(), nullable=False, default=False)
    id_funcionario = db.Column(db.Integer(), db.ForeignKey('funcionario.id'), nullable=False)
    funcionario = db.relationship('Funcionario', backref='checklists')
    id_turno = db.Column(db.Integer(), db.ForeignKey('turno.id'), nullable=False)
    turno = db.relationship('Turno', backref='checklists')


class Parametro(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(length=256), nullable=False, unique=True)


class Linha(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(length=256), nullable=False, unique=True)


class Verificacao(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    descricao = db.Column(db.String(length=45), nullable=False)
    horario = db.Column(db.DateTime(), nullable=False)
    id_parametro = db.Column(db.Integer(), db.ForeignKey('parametro.id'), nullable=False)
    parametro = db.relationship('Parametro', backref='verificacoes')
    id_checklist = db.Column(db.Integer(), db.ForeignKey('checklist.id'), nullable=False)
    checklist = db.relationship('Checklist', backref='verificacoes')


class Posto(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_linha = db.Column(db.Integer(), db.ForeignKey('linha.id'), nullable=False)
    linha = db.relationship('Linha', backref='postos')


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


@app.route('/paginageral')
def pagina_geral():
    return render_template('PagFuncionarios.html')


if __name__ == '__main__':
    app.run()