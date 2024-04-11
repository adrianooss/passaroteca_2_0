from passaroteca import db


class Aves(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_popular = db.Column(db.String(30), nullable=False)
    especie = db.Column(db.String(30), nullable=False)
    familia = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Usuarios(db.Model):
    nome = db.Column(db.String(20), primary_key=True)
    apelido = db.Column(db.String(8), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
