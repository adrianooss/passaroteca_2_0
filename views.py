from flask import  render_template, redirect, url_for, request, flash, session
from passaroteca import app, db
from models import *


@app.route('/')
def index():https://github.com/adrianooss/passaroteca_2_0.git
    lista = Aves.query.order_by(Aves.id)
    return render_template('lista.html', titulo='Aves', aves=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Nova Ave')


@app.route('/criar', methods=['POST',])
def criar():
    nome_popular = request.form['nome_popular']
    especie = request.form['especie']
    familia = request.form['familia']
    ave = Aves.query.filter_by(especie=especie).first()
    if ave:
        flash('Ave já existente!')
        return redirect(url_for('index'))

    nova_ave = Aves(nome_popular=nome_popular, especie=especie, familia=familia)
    db.session.add(nova_ave)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima = url_for('editar', id=id)))
    ave = Aves.query.filter_by(id=id).first()
    return render_template('editar.html', ave=ave, titulo='Editando')


@app.route('/atualizar', methods=['POST',])
def atualizar():
    ave = Aves.query.filter_by(id=request.form['id']).first()
    ave.nome_popular = request.form['nome_popular']
    ave.especie = request.form['especie']
    ave.familia = request.form['familia']

    db.session.add(ave)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima = url_for('deletar', id=id)))
    Aves.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Ave deletada com sucesso!')

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(apelido=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.apelido
            flash(usuario.apelido + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    '''
   if session['usuario_logado'] not in session:
        flash('Nenhum usuário logado!')
        return redirect(url_for('index'))
    else:
    '''
    session['usuario_logado'] = None
    flash('O usuário saiu da aplicação!')
    return redirect(url_for('index'))