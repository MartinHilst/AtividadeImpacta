from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client["jogos"]
collec = db["jogos_flask"]

lista = []

app = Flask(__name__)
app.config["SESSION_PERMANET"]=True
app.config["SESSION_TYPE"]="filesystem"
Session(app)

jogos=[jogo for jogo in collec.find({}, {"_id": 1,  "nome": 1, "categoria": 1, "console":1}).sort("nome",1)]

@app.route('/')
def index():
    lista=[jogo for jogo in collec.find({}, {"_id": 1,  "nome": 1, "categoria": 1, "console":1})]
        
    return render_template('index.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo', action='/criar')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    collec.insert_one({"nome": nome,"categoria": categoria,"console":console})
    return redirect('/')

@app.route('/separarCategoria')
def separarCategoria():
    jogos=[jogo for jogo in collec.find({}, {"_id": 1,  "nome": 1, "categoria": 1, "console":1}).sort("categoria",1)]

    return render_template('index.html', titulo='Jogos', jogos=jogos)

@app.route('/separarConsole')
def separarConsole():
    jogos=[jogo for jogo in collec.find({}, {"_id": 1,  "nome": 1, "categoria": 1, "console":1}).sort("console",1)]
   
    return render_template('index.html', titulo='Jogos', jogos=jogos)

@app.route('/separarNome')
def separarNome():
    jogos=[jogo for jogo in collec.find({}, {"_id": 1,  "nome": 1, "categoria": 1, "console":1}).sort("nome",1)]

    return render_template('index.html', titulo='Jogos', jogos=jogos)

@app.route('/deletar/<id>')
def deletar(id):
    idDeletar = request.view_args['id']
    collec.delete_one({ "_id": ObjectId(idDeletar) })
    print(idDeletar)      

    return redirect('/')

@app.route('/editar/<id>')
def editar(id):
    session['idEditar'] = request.view_args['id']
    idEditar = request.view_args['id']
    jogo=collec.find_one({"_id": ObjectId(idEditar)})
    return render_template('novo.html', titulo='Editar Jogo',jogo=jogo,action='/editarB')

@app.route('/editarB',methods=['POST',])
def editarB():
    id=session.get('idEditar', None)
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    collec.update_one({"_id" :ObjectId(id)},{'$set':{"nome":nome,"categoria":categoria,"console":console}})
    return redirect('/')

app.run(debug=True)