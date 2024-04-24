from flask_wtf import FlaskForm
from passaroteca import app
from wtforms import StringField, SubmitField, PasswordField, validators
import os

class FormularioAve(FlaskForm):
    nome_popular = StringField('Nome Popular',[validators.DataRequired(), validators.Length(min=1,max=30)])
    especie = StringField('Espécie', [validators.DataRequired(), validators.Length(min=1, max=30)])
    familia = StringField('Família', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    apelido = StringField('Apelido',[validators.DataRequired(), validators.Length(min=1,max=8)])
    senha = PasswordField('Senha',[validators.DataRequired(), validators.Length(min=1,max=100)])
    login = SubmitField('Login')
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'foto{id}' in nome_arquivo:
            return nome_arquivo
    return 'foto_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'foto_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))

