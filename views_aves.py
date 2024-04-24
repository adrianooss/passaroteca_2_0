from flask import render_template, redirect, url_for, request, flash, session, send_from_directory
from passaroteca import app, db
from models import Aves
import time
from helpers import recupera_imagem, deleta_arquivo, FormularioAve


@app.route('/')
def index():
    lista = Aves.query.order_by(Aves.id)
    return render_template('lista.html', titulo='Aves', aves=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioAve()
    return render_template('novo.html', titulo='Nova Ave', form=form)


@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioAve(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome_popular = form.nome_popular.data
    especie = form.especie.data
    familia = form.familia.data

    ave = Aves.query.filter_by(especie=especie).first()

    if ave:
        flash('Ave já existente!')
        return redirect(url_for('index'))

    nova_ave = Aves(nome_popular=nome_popular, especie=especie, familia=familia)
    db.session.add(nova_ave)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/foto{nova_ave.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('editar', id=id)))
    ave = Aves.query.filter_by(id=id).first()
    form = FormularioAve()
    form.nome_popular.data = ave.nome_popular
    form.especie.data = ave.especie
    form.familia.data = ave.familia
    foto_ave = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando', id=id,  foto_ave=foto_ave, form=form)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioAve(request.form)

    if form.validate_on_submit():

        ave = Aves.query.filter_by(id=request.form['id']).first()
        ave.nome_popular = form.nome_popular.data
        ave.especie = form.especie.data
        ave.familia = form.familia.data

        db.session.add(ave)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(ave.id)
        arquivo.save(f'{upload_path}/foto{ave.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima = url_for('deletar', id=id)))
    Aves.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Ave deletada com sucesso!')

    return redirect(url_for('index'))



@app.route('/upload/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('upload', nome_arquivo)