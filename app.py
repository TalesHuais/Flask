# pip install flask 
# pip install Flask-SQLAlchemy 
# pip install Flask-Migrate 
# pip install Flask-Script 
# pip install pymysql 
# flask db init 
# flask db migrate -m "Migração Inicial" 
# flask db upgrade
# flask run --debug

from flask import Flask, render_template, request, flash, redirect
app = Flask(__name__)
from database import db
from flask_migrate import Migrate
from models import Animal
app.config['SECRET_KEY'] = ['2c1685c157fe2450fda443a0753bb69f']

# drive://usuario:senha@servidor/banco_de_dados
conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/bd_animais"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/animais')
def animais():
    a = Animal.query.all()
    return render_template('animais_lista.html', dados=a)

@app.route('/animais/add')
def animais_add():
    return render_template("animais_add.html")

@app.route('/animais/save', methods=['POST'])
def animais_save():
    nome = request.form.get('nome')
    especie = request.form.get('especie')
    idade = request.form.get('idade')
    if nome and especie and idade:
        animal = Animal(nome, especie, idade)
        db.session.add(animal)
        db.session.commit()
        flash('Animal cadastrado com sucesso!!!')
        return redirect('/animais')
    else:
        flash('Preencha todos os campos')
        return redirect('/animais/add')

@app.route('/animais/remove/<int:id>')
def animais_remove(id):
    if id > 0:
        animal = Animal.query.get(id)
        db.session.delete(animal)
        db.session.commit()
        flash('Animal removido com sucesso!!!')
        return redirect('/animais')
    else:
        flash('Caminho Incorreto!')
        return redirect('/animais')
    
@app.route('/animais/edita/<int:id>')
def animais_edita(id):
    animal = Animal.query.get(id)
    return render_template("animais_edita.html", dados=animal)

@app.route('/animais/edita-save', methods=['POST'])
def animais_edita_save():
    nome = request.form.get('nome')
    especie = request.form.get('especie')
    idade = request.form.get('idade')
    id = request.form.get('id')
    if id and nome and especie and idade:
        animal = Animal.query.get(id)
        animal.nome = nome
        animal.especie = especie
        animal.idade = idade
        db.session.commit()
        flash('Dados atualizados com sucesso!')
        return redirect('/animais')
    else:
        flash('Faltando dados!!')
        return redirect('/animais')

if __name__ == '__main__':
    app.run()