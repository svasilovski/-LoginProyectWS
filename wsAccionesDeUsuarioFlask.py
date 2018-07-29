#!flask/bin/python
# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/xmlrpc.server.html
import os, sys
import logging
from flask import request, Flask, jsonify, abort, make_response

sys.path.insert(0, os.path.realpath('pyAuxiliares'))
import ConnectionDBClass
import UsuariosClass

app = Flask(__name__)

# initialize the log settings
logging.basicConfig(filename='logs/appWSServices.log',level=logging.INFO)

dbConnection = 'db/dbLogin.sqlite'

def crearTablas():
	try:
		d=ConnectionDBClass.ConnectionDBClass(dbConnection)
		conn=d.connection_sqlite()
		print('Inicializar base de datos')
		usrConn = UsuariosClass.UsuariosClass(conn);
		usrConn.create_db()
	except Exception as e:
		logging.error('Error occurrido al crearTablas {0}'.format(e))

crearTablas()

@app.route('/')
@app.route('/usuario')
def index():
	return "El servicio se está ejecutando."

@app.route('/usuario/agregarUsuario', methods=['POST'])
def agregarUsuario():
	"""	Inserta un usuario en la base de datos
		Args:
			usuario 		(str)	Usuario a ingresar.
			password 		(str)   Password a ingresar.
		Returns:
			0 = OK
			1 = El usuario ya existe
			2 = Exception
	"""
	if not request.json or not 'usuario' or not 'password' in request.json:
		return jsonify({'status': 'Error en la recepción de datos.'});

	usuario=request.json['usuario']
	password=request.json['password']

	d=ConnectionDBClass.ConnectionDBClass(dbConnection)
	conn=d.connection_sqlite()
	usrConn = UsuariosClass.UsuariosClass(conn)
	task=usrConn.insert_user(usuario, password)
	return jsonify({'data':{'usuario': usuario, 'status': task }, 'references': ['OK', 'El usuario ya existe', 'Exception']}), 201

@app.route('/usuario/eliminarUsuario', methods=['POST'])
def eliminarUsuario():
	"""	Baja del usuario enviado
		Args:
			usuario 		(str)	Usuario a ingresar.
			password 		(str)   Password a ingresar.
		Returns:
			0 = OK
			1 = El usuario no existe.
			2 = Exception
			3 = Password incorrecta
	"""
	if not request.json or not 'usuario' or not 'password' in request.json:
		return jsonify({'status': 'Error en la recepción de datos.'});

	usuario=request.json['usuario']
	password=request.json['password']

	d=ConnectionDBClass.ConnectionDBClass(dbConnection)
	conn=d.connection_sqlite()
	usrConn = UsuariosClass.UsuariosClass(conn)
	task = usrConn.baja_usuario(usuario, password)
	return jsonify({'data':{'usuario': usuario, 'status': task}, 'references': ['OK', 'El usuario ya existe', 'Exception', 'Password incorrecta']}), 201

@app.route('/usuario/bloquearDesbloquearUsuario', methods=['POST'])
def bloquearDesbloquearUsuario():
	"""	Habilita o inhabilita un usuario
		Args:
			usuario 		(str)	Usuario a ingresar.
			habilitado 		(int)   Habilia/deshabilita un usuario.
		Examples:
			habilitado:
				1= Usuario habilitado
				0= Usuario inhabilitado
		Returns:
			0 = OK
			1 = No existe Usuario
			2 = Exception
			3 = Ya se encuentra en el estado a cambiar
	"""
	if not request.json or not 'usuario' or not 'habilitado' in request.json:
		return jsonify({'status': 'Error en la recepción de datos.'});

	usuario=request.json['usuario']
	habilitado=request.json['habilitado']

	d=ConnectionDBClass.ConnectionDBClass(dbConnection)
	conn=d.connection_sqlite()
	usrConn = UsuariosClass.UsuariosClass(conn)
	task = usrConn.habilitar_usuario(usuario, habilitado)
	return jsonify({'data':{'usuario': usuario, 'habilitado': habilitado, 'status': task}, 'references': ['OK', 'No existe Usuario', 'Exception', 'Ya se encuentra en el estado a cambiar']}), 201

@app.route('/usuario/actualizarUsuario', methods=['POST'])
def actualizarUsuario():
	"""	Actualiza la password de un usuario en la base de datos.
		Args:
			usuario 		(str)	Usuario a ingresar.
			password 		(str)   Password a anterior.
			newPassword 		(str)   Password nueva.
			passwordConfirm		(str)   Password nueva repetida.
		Returns:
			0 = OK
			1 = Las Password no coinciden
			2 = Exception
			3 = El usuario no existe
			4 = Password incorrecta
	"""
	if not request.json or not 'usuario' or not 'password' or not 'nuevaPassword' or not 'passwordRepetida' in request.json:
		return jsonify({'status': 'Error en la recepción de datos.'});

	usuario=request.json['usuario']
	password=request.json['password']
	nuevaPassword=request.json['nuevaPassword']
	passwordRepetida=request.json['passwordRepetida']

	d=ConnectionDBClass.ConnectionDBClass(dbConnection)
	conn=d.connection_sqlite()
	usrConn = UsuariosClass.UsuariosClass(conn)
	task = usrConn.update_user(usuario, password, nuevaPassword, passwordRepetida)
	return jsonify({'data':{'usuario': usuario, 'status': task}, 'references': ['OK', 'Las Password no coinciden', 'Exception', 'El usuario no existe', 'Password incorrecta']}), 201

@app.route('/usuario/validarUsuario', methods=['POST'])
def validarUsuario():
	"""	Valida las credenciales enviadas
		Args:
			usuario 		(str)	Usuario a ingresar.
			password 		(str)   Password a anterior.
		Returns:
			0 = OK
			1 = El usuario no existe
			2 = Exception
			3 = Password correcta
			4 = Password incorrecta
	"""
	if not request.json or not 'usuario' or not 'password' in request.json:
		return jsonify({'status': 'Error en la recepción de datos.'});

	usuario=request.json['usuario']
	password=request.json['password']

	d=ConnectionDBClass.ConnectionDBClass(dbConnection)
	conn=d.connection_sqlite()
	usrConn = UsuariosClass.UsuariosClass(conn)
	task = usrConn.validate_user(usuario, password)
	return jsonify({'data':{'usuario': usuario, 'status': task}, 'references': ['OK', 'El usuario no existe', 'Exception', 'Password correcta', 'Password incorrecta']}), 201

@app.route('/usuario/listarUsuarios', methods=['GET'])
def listarUsuarios():
	"""	Retorna una lista de usuarios. """
	d=ConnectionDBClass.ConnectionDBClass(dbConnection)
	conn=d.connection_sqlite()
	usrConn = UsuariosClass.UsuariosClass(conn)
	lstUser = usrConn.listar_usuarios()
	task = [{"id":i[0], "user_email":i[1]} for i in lstUser]
	return jsonify({'data': task}), 201


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.debug=True
	app.run(host= '0.0.0.0')
	#app.run(debug=True)
	# Run the server's main loop
	#try:
#		print('Use Control-C to exit')
#	except KeyboardInterrupt:
#		sys.path.remove(os.path.realpath('pyAuxiliares'))
#		print('Exiting')