from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def pag_inicial():
    return render_template('PagInicial.html')


if __name__ == '__main__':
    app.run()
