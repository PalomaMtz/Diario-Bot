#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import Form, SelectField, StringField, PasswordField, validators

class CommentForm(Form):
	username= StringField('Usuario:', [validators.Required('Ingrese un Usuario')])
	password= PasswordField('Password:', [validators.Required('Es necesario ingresar el Password')])


class Registro_Form(Form):
	username= StringField('Usuario:', [validators.Required('Ingrese un Usuario'), validators.Length(min=3, max=100)])
	password= PasswordField('Password:', [validators.Required('Es necesario ingresar el Password'), validators.Length(min=8, max=30)])
	password_2 = PasswordField('Repetir Password: ', [validators.EqualTo('password', message='Las contraseñas no coinciden')] )
	apellido= StringField('Apellido:', [validators.Required('Ingrese apellido'),validators.Length(min=3, max=50)])
	genero= SelectField('Sexo:', choices=[('', 'Seleccione:'), ('F', 'Femenino'), ('M', 'Masculino')])
