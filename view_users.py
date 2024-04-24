from passaroteca import app
from flask import render_template, redirect, url_for, request, flash, session
from models import Usuarios
from helpers import FormularioUsuario

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(apelido=form.apelido.data).first()
    if usuario:
        if form.senha.data == usuario.senha:
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