from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["jogos"]
collec = db["jogos_flask"]

lista = []

app = Flask(__name__)

@app.route('/')
def index():
    lista=[jogo for jogo in collec.find({}, {"_id": 0,  "nome": 1, "categoria": 1, "console":1})]
        
    return render_template('index.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    collec.insert_one({"nome": nome,"categoria": categoria,"console":console})
    return redirect('/')

@app.route('/separarCategoria')
def separarCategoria():
    jogos=[jogo for jogo in collec.find({}, {"_id": 0,  "nome": 1, "categoria": 1, "console":1}).sort("categoria",1)]

    return render_template('index.html', titulo='Jogos', jogos=jogos)

@app.route('/separarConsole')
def separarConsole():
    jogos=[jogo for jogo in collec.find({}, {"_id": 0,  "nome": 1, "categoria": 1, "console":1}).sort("console",1)]
   
    return render_template('index.html', titulo='Jogos', jogos=jogos)

@app.route('/separarNome')
def separarNome():
    jogos=[jogo for jogo in collec.find({}, {"_id": 0,  "nome": 1, "categoria": 1, "console":1}).sort("nome",1)]

    return render_template('index.html', titulo='Jogos', jogos=jogos)

app.run(debug=True)