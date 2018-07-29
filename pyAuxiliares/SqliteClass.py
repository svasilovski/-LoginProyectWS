#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import logging

class SqliteClass(object):
	"""	Consultas genericas a la base de datos de sqlite. 
		Args:
			conn (sqlite3.connect): Nombre de la base de datos a ejecutar/crear
		Attributes:
			conn (sqlite3.connect): Nombre de la base de datos a ejecutar/crear
	"""
	
	def __init__(self, conn):
		"""	Inicializa la clase instanciada. """
		self.conn = conn
		# initialize the log settings
		logging.basicConfig(filename='../logs/appSqliteClasss.log',level=logging.INFO)

	def get_exist_table(self, tipo, nombre):
		"""	Valida si existe la tabla.
			Args:
				tipo (str) 		Tipo de elemento a buscar (table, index, etc)
				nombre (str) 	Nombre del tipo a validar su existencia
			Returns:
				-1 Error
				 0 La tabla no existe
				 1 La tabla existe
				>1 Ambiguo
		"""
		ret = -1
		try:
			query = "SELECT COUNT(*) FROM sqlite_master WHERE type = '{0}' AND name = '{1}';".format(tipo, nombre)
			cursor = self.conn.cursor()
			cursor.execute(query)
			ret = cursor.fetchone()[0]
			cursor.close()
		except Exception as e:
			logging.error("get_exist_table error: {0}".format(e))
		return ret

	def get_exist_campo_in_table(self, tableName, campos):
		"""	Valida si existe la tabla.
			Args:
				tableName (str) Nombre de la tabla
				campos (str) 	Campos separados por ","
			Returns:
				-1 Error
				 0 OK
				>1 Hay vampos que no existen
		"""
		ret = 0
		try:
			query = "PRAGMA table_info('{0}')".format(tableName)
			cursor = self.conn.cursor()
			cursor.execute(query)
			datos = cursor.fetchall()
			print(len(datos))
			if(len(datos)>0):
				for d in datos:
					nombre=d[1]
					if campos.contains(d[1]):
						ret+=1
			else:
				ret = len(campos.split(","))
			cursor.close()
		except Exception as e:
			logging.error("get_exist_campo_in_table error: {0}".format(e))
			ret -1
		return ret

	def create_table(self, tableName, campos):
		"""	Cres las tablas de la base de datos si no existen.
			Args:
				tableName (string)	Nombre de la tabla
				campos (string)		Campos y propiedades
			Examples:
				campos 				campo1 tipo prop1 prop2, campo2 tipo prop1 prop2,...
			Returns:
				0 = Se creo la tabla
				1 = La tabla existe
				2 = Exception
		"""
		ret = 0
		try:
			cant = self.get_exist_table('table', tableName)
			if cant==0:
				query = "CREATE TABLE {0}({1});".format(tableName, campos)
				cursor = self.conn.cursor()
				cursor.execute(query)
				cursor.close()
			else:
				ret = 1
		except Exception as e:
			logging.error("create_table error: {0}".format(e))
			ret = 2
		return ret

	def create_Index(self, indexName, tableName, campos):
		"""	Cres las tablas de la base de datos si no existen.
			Args:
				indexName (string)	Nombre del indice
				tableName (string)	Nombre de la tabla que se va a aplicar
				campos (string)		Campos a los que se crearan el indice
			Examples:
				campos 		campo1,campo2,campo3,...
			Returns:
				0 = Se creo el indice
				1 = El indice existe
				2 = Hay campos que no existen
				3 = Exception
		"""
		# Recorrer los campos
		# validar existencia de campos
		# Si existe crear el indice
		ret = 0
		try:
			cant = self.get_exist_table('index', indexName)
			if cant==0:
				cant = self.get_exist_campo_in_table(tableName, campos)
				if cant == 0:
					query = "CREATE INDEX {0} ON {1} ({2});".format(indexName, tableName, campos)
					cursor = self.conn.cursor()
					cursor.execute(query)
					cursor.close()
				else:
					ret = 2
			else:
				ret = 1
		except Exception as e:
			logging.error("create_Index error: {0}".format(e))
			ret = 3
		return ret

	def listar_datos(self, nombreTabla, campos='*', filtros = None):
		"""	Obriene una lista de registros
			Args:
				campos (string)			Listado de campos por defecto por efecto es "*".
				nombreTabla (string)	Nombre de la tabla.
				filtros (string)		Filtros que se van a aplicar.
			Returns:
				Array de registros [(*,*,*,*),(*,*,*,*)]
		"""
		ret=[]
		try:
			query = "SELECT {0} FROM {1}".format(campos, nombreTabla)
			if filtros is not None:
				query += " WHERE {0}".format(filtros)
			query += ";"
			cursor = self.conn.cursor()
			cursor.execute(query)
			ret = cursor.fetchall()
			cursor.close()
		except Exception as e:
			logging.error("listar_datos error: {0}".format(e))
		return ret

	def insertar_datos(self, nombreTabla, campos, valores):
		"""	Inserta un registro un la tabla enviada de la conexión de la base de datos
			Args:
				nombreTabla (string)	Nombre de la tabla.
				campos 		(string)	Listado de campos separados por ","
				valores 	(string)	Valores a asignar separados por ","
			Returns:
				0 = OK
				1 = Exception
		"""
		ret=0;
		try:
			query = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(nombreTabla, campos, valores)
			cursor = self.conn.cursor()
			cursor.execute(query)
			self.conn.commit()
			cursor.close()
		except Exception as e:
			logging.error("insertar_datos error: {0}".format(e))
			ret=1
		return ret

	def actualizar_datos(self, nombreTabla, camposValor, filtros):
		"""	Actualiza un registro un la tabla enviada de la conexión de la base de datos
			Args:
				nombreTabla (string)	Nombre de la tabla.
				camposValor	(string)	Datos a cambiar.
				filtros 	(string)	En que resistro va a aplicarse
			Returns:
				0 = OK
				1 = Exception
		"""
		ret=0;
		try:
			if filtros is None:
				filtros = '1=1'
			query = "UPDATE {0} SET {1} WHERE {2};".format(nombreTabla, camposValor, filtros)
			cursor = self.conn.cursor()
			cursor.execute(query)
			self.conn.commit()
			cursor.close()
		except Exception as e:
			logging.error("actualizar_datos error: {0}".format(e))
			ret=1
		return ret