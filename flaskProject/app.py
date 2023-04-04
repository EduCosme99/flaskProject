from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/login')
def pag_inicial():
    return render_template('PagInicial.html')


@app.route('/geral')
def login_geral():
    return render_template('LoginGeral.html')

if __name__ == '__main__':
    app.run()
