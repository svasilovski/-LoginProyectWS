#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import binascii
import uuid
import hashlib
import SqliteClass
import logging

class UsuariosClass(object):
	"""	Crea la tabla usuarios si no existe y realiza operaciones en la misma. 
		Args:
			conn (sqlite3.connect): Nombre de la base de datos a ejecutar/crear
		Attributes:
			conn (sqlite3.connect): Nombre de la base de datos a ejecutar/crear
	"""
	def __init__(self, conn):
		"""	Inicializa la clase instanciada. """
		self.SqliteClass = SqliteClass.SqliteClass(conn)
		# initialize the log settings
		logging.basicConfig(filename='../logs/appUsuarioClass.log',level=logging.INFO)

	def create_db(self):
		"""	Crea las tablas de la base de datos si no existen y los indices.
			Returns:
				0 OK
				1 Hay campos que no existen para crear el indice
				2 Error al crear el indice
				3 Problemas al crear la tabla
				4 Exception
		"""
		retFun = [0,0]
		ret = 0
		try:
			retFun[0] = self.SqliteClass.create_table('users', 'id INTEGER PRIMARY KEY ASC NOT NULL,user_email TEXT(50) NOT NULL,user_password TEXT(279) NOT NULL,fecha_alta DATE,fecha_baja DATE,habilitado BINARY(1)')
			if retFun[0] != 2:
				#retFun[1] = self.SqliteClass.create_Index('index_users', 'users', 'user_email')
				if ((retFun[0] == 0  and retFun[1] == 2) or (retFun[0] == 1  and retFun[1] == 2)):
					ret = 1
				elif ((retFun[0] == 0  and retFun[1] == 3) or (retFun[0] == 1  and retFun[1] == 3)):
					ret = 2
			else:
				ret = 3
		except Exception as e:
			logging.error("create_db error: {0}".format(e))
			ret = 4
		return ret

	def hash_password(self, password):
		"""	Genera un hash random para la password privada
			Args:
				password (str)	Recive una password
			Returns:
				Retorna un hash entre una password privada y la clave.
		"""
		salt = uuid.uuid4().hex
		return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

	def check_password(self, hashed_password, user_password):
		"""	Chequea usuario y password y retorna un valor booleano
			Args:
				hashed_password (str)	Recive el hash de la password.
				user_password	(str)	Recibe la password a comparar.
			Returns:
				Retorna un hash entre una password privada y la clave.
		"""
		password, salt = hashed_password.split(':')
		return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

	def existe_usuario(self, usuario):
		"""	Valida si existe el usuario.
			Args:
				usuario (str)	Usuario a validar.
			Returns:
				Array de usuarios [(*,*,*,*),(*,*,*,*)]
		"""
		ret=[]
		try:
			filtro = "user_email = '{0}' AND fecha_baja IS NULL".format(usuario)
			ret = self.SqliteClass.listar_datos('users', 'id, user_email, user_password, fecha_alta, fecha_baja, habilitado', filtro)
		except Exception as e:
			logging.error("existe_usuario error: {0}".format(e))
		return ret

	def insert_user(self, usuario, password):
		"""	Inserta un usuario en la base de datos
			Args:
				usuario 	(str)	Usuario a ingresar.
				password 	(str)   Password a ingresar.
			Returns:
				0 = OK
				1 = El usuario ya existe
				2 = Exception
		"""
		ret=0;
		try:
			d = self.existe_usuario(usuario)
			if len(d)==0:
				private_key = self.hash_password(password)
				ret = self.SqliteClass.insertar_datos('users', 'user_email, user_password, fecha_alta, fecha_baja, habilitado', "'{0}', '{1}',datetime('now','localtime'),NULL,1".format(usuario, private_key))
				if ret!=0:
					ret = 2
			else:
				ret=1
		except Exception as e:
			logging.error("insert_user error: {0}".format(e))
			ret=2
		return ret

	def update_user(self, usuario, password, newPassword, passwordConfirm):
		"""	Actualiza la password de un usuario en la base de datos.
			Args:
				usuario 		(str)	Usuario a ingresar.
				password 		(str)   Password a anterior.
				newPassword 	(str)   Password nueva.
				passwordConfirm	(str)   Password nueva repetida.
			Returns:
				0 = OK
				1 = Las Password no coinciden
				2 = Exception
				3 = El usuario no existe
				4 = Password incorrecta
		"""
		ret= 0
		try:
			d = self.existe_usuario(usuario)
			if len(d)>0:
				db_key = d[0][2]
				if self.check_password(db_key, password):
					if newPassword==passwordConfirm:
						private_key = self.hash_password(newPassword)
						strSetear = "user_password='{0}'".format(private_key)
						filtro = "id IN (SELECT id FROM {0} WHERE user_email='{1}')".format('users', usuario)
						ret = self.SqliteClass.actualizar_datos('users', strSetear, filtro)
						if ret == 1:
							ret = 2
					else:
						ret = 1
				else:
					ret=4
			else:
				ret = 3
		except Exception as e:
			logging.error("update_user error: {0}".format(e))
			ret = 2
		return ret

	def habilitar_usuario(self, usuario, habilitar=1):
		"""	Habilita o inhabilita un usuario
			Args:
				usuario 		(str)	Usuario a ingresar.
				habilitar 		(int)   Habilia/deshabilita un usuario.
			Examples:
					inhabilitados:
						1= Usuario habilitado
						0= Usuario inhabilitado
			Returns:
				0 = OK
				1 = No existe Usuario
				2 = Exception
				3 = Ya se encuentra en el estado a cambiar
		"""
		ret= 0
		try:
			d = self.existe_usuario(usuario)
			if len(d)>0:
				if d[0][5] != habilitar:
					strSetear = "habilitado='{0}'".format(habilitar)
					filtro = "id IN (SELECT id FROM {0} WHERE user_email='{1}')".format('users', usuario)
					ret = self.SqliteClass.actualizar_datos('users', strSetear, filtro)
					if ret == 1:
						ret = 2
				else:
					ret = 3
			else:
				ret=1
		except Exception as e:
			logging.error("habilitar_usuario error: {0}".format(e))
			ret = 2
		return ret

	def baja_usuario(self, usuario, password):
		"""	Baja del usuario enviado
			Args:
				usuario 		(str)	Usuario a ingresar.
				password 		(str)   Password a anterior.
			Returns:
				0 = OK
				1 = El usuario no existe.
				2 = Exception
				3 = Password incorrecta
		"""
		ret= 0
		try:
			d = self.existe_usuario(usuario)
			if len(d)>0:
				db_key = d[0][2]
				if self.check_password(db_key, password):
					filtro = "id IN (SELECT id FROM {0} WHERE user_email='{1}')".format('users', usuario)
					ret = self.SqliteClass.actualizar_datos('users', "fecha_baja=datetime('now','localtime')", filtro)
					if ret == 1:
						ret = 2
				else:
					ret=3
			else:
				ret=1
		except Exception as e:
			logging.error("baja_usuario error: {0}".format(e))
			ret = 2
		return ret

	def listar_usuarios(self, inhabilitados = -1):
		"""	Retorna una lista de usuarios.
			Args:
				inhabilitados (number)	Indica si queremos los habilitados-inhabilitados o todos.
			Examples:
				inhabilitados:
					-1 	todos
					1 	habilitados
					2	inhabilitados
			Returns:
				Array de usuarios [(*,*,*,*),(*,*,*,*)]
		"""
		ret=[]
		try:
			filtro = "fecha_baja IS NULL"
			if inhabilitados>-1:
				filtro += "AND habilitado={0}".format(inhabilitados)

			ret = self.SqliteClass.listar_datos('users', 'id, user_email', filtro)
		except Exception as e:
			logging.error("listar_usuarios error: {0}".format(e))
		return ret

	def validate_user(self, usuario, password):
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
		ret=0;
		try:
			d = self.existe_usuario(usuario)
			if len(d)>0:
				db_key = d[0][2]
				if self.check_password(db_key, password):
					ret=3
				else:
					ret=4
			else:
				ret=1
		except Exception as e:
			logging.error("validate_user error: {0}".format(e))
			ret=2
		return ret