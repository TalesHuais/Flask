from database import db

class Animal(db.Model):
    __tablename__ = "animal"
    id_animal = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    especie = db.Column(db.String(100))
    idade = db.Column(db.Integer)

    def __init__(self, nome, especie, idade):
        self.nome = nome
        self.especie = especie
        self.idade = idade

    def __repr__(self):
        return "<Animal {}>".format(self.nome)