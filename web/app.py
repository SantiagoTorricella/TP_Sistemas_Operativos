import os

from flask import Flask, flash, redirect, render_template, request
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
# firma la cookie donde viajan los mensajes flash
app.secret_key = "tp-libros"

# credenciales desde las env vars del docker-compose; el root user vive en la DB "admin"
client = MongoClient(
    host=os.environ["MONGO_HOST"],
    port=27017,
    username=os.environ["MONGO_USER"],
    password=os.environ["MONGO_PASSWORD"],
    authSource="admin",
)
coleccion = client[os.environ["MONGO_DB"]]["libros"]

# el id de cada libro es unico e irrepetible
coleccion.create_index("id", unique=True)

# campo del libro -> tipo con el que se guarda en Mongo
CAMPOS = {
    "id": int,
    "titulo": str,
    "cantidad_paginas": int,
    "editorial": str,
    "isbn": str,
    "costo_usd": float,
}


def leer_form(form):
    """HTML manda todo como texto, esto convierte a los tipos adecuados"""
    datos = {}
    for campo, tipo in CAMPOS.items():
        valor = form.get(campo, "").strip()
        if not valor:
            raise ValueError(f"El campo {campo} es obligatorio")
        try:
            datos[campo] = tipo(valor)
        except ValueError:
            raise ValueError(f"El campo {campo} debe ser numerico")
    return datos


@app.route("/")
def index():
    libros = coleccion.find().sort("id")
    return render_template("index.html", libros=libros)


@app.route("/libros", methods=["POST"])
def crear():
    try:
        datos = leer_form(request.form)
        coleccion.insert_one(datos)
        flash(f"Libro {datos['id']} agregado")
    except ValueError as e:
        flash(str(e))
    except DuplicateKeyError:
        flash(f"Ya existe un libro con id {datos['id']}")
    return redirect("/")
