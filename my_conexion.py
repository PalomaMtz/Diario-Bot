#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import mysql.connector
'''
base de datos: diario_bot
tabla: usuarios
    columnas: 
    usuario, clave Primaria varchar(100)
    apellido	varchar(50)
    genero	varchar(10)
    password	varchar(30

'''

DB_HOST = 'localhost' 
DB_USER = 'root' 
DB_PASS = '1234root' 
DB_NAME = 'diario_bot' 

def run_query(query):

    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 

    conn = MySQLdb.connect(*datos) 
    cursor = conn.cursor() 

    cursor.execute(query) 
    if query.startswith('SELECT'):
        date = cursor.fetchall() 
        if not date:
            data=None
        else:
            for i in date:
                data = i[0]
    elif query.startswith('INSERT'):
        data = "registrado" 


    conn.commit() 
    cursor.close()                 
    conn.close() 
 
    return data


def buscar(usuario):
    consulta = "SELECT password FROM `usuarios` WHERE usuario = '%s'" %usuario
    dato = run_query(consulta)  
    return dato

def agregar(usuario,apellido,genero,password):
    consulta = "INSERT INTO `usuarios` (`usuario`, `apellido`, `genero`, `password`) VALUES ('%s', '%s', '%s', '%s' )" % (usuario, apellido,genero,password)
    dato = run_query(consulta)
    return dato
