from flask import Flask

# mod_wsgi lo tiene que importar como "application"
app = Flask(__name__)


@app.route("/")
def index():
    return "Hola desde Apache + Flask"
