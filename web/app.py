import os

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# credenciales desde las env vars del docker-compose; el root user vive en la DB "admin"
client = MongoClient(
    host=os.environ["MONGO_HOST"],
    port=27017,
    username=os.environ["MONGO_USER"],
    password=os.environ["MONGO_PASSWORD"],
    authSource="admin",
)
coleccion = client[os.environ["MONGO_DB"]]["libros"]


@app.route("/")
def index():
    return f"Conectado a Mongo, {coleccion.count_documents({})} libros"
