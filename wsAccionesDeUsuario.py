#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/xmlrpc.server.html
import os, sys
import logging

# initialize the log settings
logging.basicConfig(filename='logs/appWSServices.log',level=logging.INFO)

# sys.path.insert(0, os.getcwd())
# print(os.path.realpath('pyAuxiliares'))
sys.path.insert(0, os.path.realpath('pyAuxiliares'))
import ConnectionDBClass
import UsuariosClass

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


dbConnection = 'db\dbLogin.sqlite'

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/usuario',)

# Create server
with SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler) as server:
	server.register_introspection_functions()

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
	
	# Register an instance; all the methods of the instance are
	# published as XML-RPC methods (in this case, just 'mul').
	class Acciones:
		def agregarUsuario(self, usuario, password):
			"""	Inserta un usuario en la base de datos
				Args:
					usuario 		(str)	Usuario a ingresar.
					password 		(str)   Password a ingresar.
				Returns:
					0 = OK
					1 = El usuario ya existe
					2 = Exception
			"""

			d=ConnectionDBClass.ConnectionDBClass(dbConnection)
			conn=d.connection_sqlite()
			usrConn = UsuariosClass.UsuariosClass(conn)
			return usrConn.insert_user(usuario, password)

		def eliminarUsuario(self, usuario, password):
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

			d=ConnectionDBClass.ConnectionDBClass(dbConnection)
			conn=d.connection_sqlite()
			usrConn = UsuariosClass.UsuariosClass(conn)
			return usrConn.baja_usuario(usuario, password)

		def bloquearDesbloquearUsuario(self, usuario, habilitado):
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

			d=ConnectionDBClass.ConnectionDBClass(dbConnection)
			conn=d.connection_sqlite()
			usrConn = UsuariosClass.UsuariosClass(conn)
			return usrConn.habilitar_usuario(usuario, habilitado)

		def actualizarUsuario(self, usuario, password, nuevaPassword, passwordRepetida):
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

			d=ConnectionDBClass.ConnectionDBClass(dbConnection)
			conn=d.connection_sqlite()
			usrConn = UsuariosClass.UsuariosClass(conn)
			return usrConn.update_user(usuario, password, nuevaPassword, passwordRepetida)

		def validarUsuario(self, usuario, password):
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
			
			d=ConnectionDBClass.ConnectionDBClass(dbConnection)
			conn=d.connection_sqlite()
			usrConn = UsuariosClass.UsuariosClass(conn)
			return usrConn.validate_user(usuario, password)

		def listarUsuarios(self):
			"""	Retorna una lista de usuarios.
				Args:
					inhabilitados 		(int)	Indica si queremos los habilitados-inhabilitados o todos.
				Examples:
					inhabilitados:
						-1 	todos
						1 	habilitados
						2	inhabilitados
				Returns:
					Array de usuarios [(id, nombre)[,(id, nombre)]
			"""

			d=ConnectionDBClass.ConnectionDBClass(dbConnection)
			conn=d.connection_sqlite()
			usrConn = UsuariosClass.UsuariosClass(conn)
			return usrConn.listar_usuarios()

	server.register_instance(Acciones())

	# Run the server's main loop
	#server.serve_forever()
	try:
		print('Use Control-C to exit')
		server.serve_forever()
	except KeyboardInterrupt:
		sys.path.remove(os.path.realpath('pyAuxiliares'))
		print('Exiting')