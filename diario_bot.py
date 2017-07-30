
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from flask import Flask, redirect, url_for, render_template, session, request
from flask_socketio import emit, SocketIO
from tinydb import TinyDB, Query
import argparse
import dateparser
import datetime
import os
import re
from docx import Document
import json
import shutil
import forms
import MySQLdb
import my_conexion
import InteligenciaBot
import convertWord

from wtforms import Form, SelectField, StringField, PasswordField, validators

app = Flask(__name__)
# Habilita sockets in aplicacion Flaks
socketio = SocketIO(app)

STATES={}
def new_state():
    return {
        'mama':False,
        'papa':False,
        'amigo': False,
        'mascota': False,
        'trabajo': False,
        'escuela': False,
        'vez' : 0,
    }

db = TinyDB('conversations.json')
Usuario= Query()

@app.route('/', methods = ['GET','POST'])
def login():
	comment_form = forms.CommentForm(request.form)
	usuario=comment_form.username.data
	contra= comment_form.password.data

	if request.method=='POST' and comment_form.validate():
		info=my_conexion.buscar(usuario)
		user=db.search(Usuario.user == usuario)
		print(info,contra)
		if not info == contra:
			return render_template('index.html', form=comment_form)
		else:
			user=user[0]
	    	conv=user['conversations']
	    	db.update({'conversations':conv},eids=[user.eid])
	    	STATES[usuario]=new_state()	
	    	return render_template('chat.html',username=usuario)
	return render_template('index.html', form=comment_form)

@app.route('/registro')
def registrar():
	data_registro=forms.Registro_Form(request.form)
	return render_template('registro.html', form=data_registro)

@app.route('/export')
def exportar():
	convertWord.exportar()
	return redirect(url_for('login'))	

@app.route('/cerrar')
def cerrar_sesion():
	#session.close()
	return redirect(url_for('login'))

@app.route('/guardar_usuario', methods = ['GET','POST'])
def guardar_usuario():

	comment_form = forms.Registro_Form(request.form)
	username=comment_form.username.data
	lastname= comment_form.apellido.data
	gender= comment_form.genero.data
	password= comment_form.password.data

	#print(username,password,lastname,gender)
	busqueda=my_conexion.buscar(username)
	print(busqueda)
	if busqueda != None:
		return redirect(url_for('registrar'))

	if request.method=='POST' and comment_form.validate():
		info = my_conexion.agregar(username,lastname,gender,password)
		
		#crear una tabla para las imagenes de cada usuario

		if info=='registrado':
			user=db.insert({'user':username, 'conversations':[[]]})
			return redirect(url_for('login'))
		else:
			return redirect(url_for('registrar'))
	else:
		return redirect(url_for('registrar'))


# Mensajes con chat
@socketio.on('message', namespace='/ask')
def mensajes(message):
    username,message_=message['data'].split(':',1)
    user=db.search(Usuario.user == username)
    user=user[0]
    ans = InteligenciaBot.generarRespuesta(message_, STATES[username],username,)
   
    conv=user['conversations']
    conv[-1].append({'msg':message_,'ans':ans})
    print(message_)
    db.update({'conversations':conv},eids=[user.eid])
    emit('response', {'data': ans})


if __name__ == '__main__':
    p = argparse.ArgumentParser("pyAIML")
    p.add_argument("--host",default="127.0.0.1",
            action="store", dest="host",
            help="Root url [127.0.0.1]")
    p.add_argument("--port",default=5000,type=int,
            action="store", dest="port",
            help="Port url [500]")
    p.add_argument("--debug",default=False,
            action="store_true", dest="debug",
            help="Use debug deployment [Flase]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts = p.parse_args()
    socketio.run(app,
	    debug=opts.debug,
            host=opts.host,
            port=opts.port)

#app.run()