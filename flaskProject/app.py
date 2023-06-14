from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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


def get_turno_atual():
    now = datetime.now()
    turno_atual = Turno.query.filter(Turno.inicio_turno <= now, Turno.fim_turno <= now).first()
    return turno_atual


@app.route('/excluir_parametro/<int:parametro_id>', methods=['POST'])
def excluir_parametro(parametro_id):
    parametro = Parametro.query.get_or_404(parametro_id)
    db.session.delete(parametro)
    db.session.commit()
    return redirect(url_for('lista_parametros'))


@app.route('/')
@app.route('/login')
def pag_inicial():
    return render_template('PagInicial.html')


@app.route('/login_geral', methods=['GET', 'POST'])
def login_geral():
    if request.method == 'POST':
        password = request.form['password']

        funcionario = Funcionario.query.filter_by(password=password).first()

        if funcionario:
            return redirect(url_for('checklists'))
        else:
            flash('Credenciais inválidas. Tente novamente', 'error')

    return render_template('LoginGeral.html')


@app.route('/login_supervisores', methods=['GET', 'POST'])
def login_supervisores():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        funcionario = Funcionario.query.filter_by(email=email, password=password).first()

        if funcionario:
            return redirect(url_for('supervisor'))
        else:
            flash('Credenciais inválidas. Tente novamente', 'error')

    return render_template('LoginSupervisores.html')


@app.route('/pre_checklist')
def pre_checklist():
    return render_template('ChecklistFunc.html')


@app.route('/pos_checklist')
def pos_checklist():
    return render_template('Checklist.html')


@app.route('/lista_funcionarios')
def lista_funcionarios():
    funcionarios = Funcionario.query.all()
    return render_template('ListaFuncionarios.html', funcionarios=funcionarios)


@app.route('/lista_parametros')
def lista_parametros():
    parametros = Parametro.query.all()
    return render_template('ListaParametros.html', parametros=parametros)


@app.route('/supervisor')
def supervisor():
    turno_atual = get_turno_atual()
    funcionarios = Funcionario.query.all()
    return render_template('Supervisores.html', turno_atual=turno_atual, funcionarios=funcionarios)


@app.route('/adicionar_funcionario')
def adicionar_funcionario():
    return render_template('AdicionarFuncionario.html')


@app.route('/adicionar_supervisor')
def adicionar_supervisor():
    return render_template('AdicionarSupervisor.html')


@app.route('/adicionar_operadorvq')
def adicionar_operadorvq():
    return render_template('AdicionarOperadorVQ.html')


@app.route('/observacao')
def observacao():
    return render_template('Observacoes.html')


@app.route('/validacao')
def validacao():
    return render_template('Validaçao.html')


if __name__ == '__main__':
    app.run()