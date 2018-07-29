#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import logging

class ConnectionDBClass(object):
	"""	Define la base de datos.
		Args:
			fileName (str): Nombre de la base de datos a ejecutar/crear
		Attributes:
			fileName (str): Nombre de la base de datos a ejecutar/crear
	"""
	
	def __init__(self, fileName):
		"""	Inicializa la clase instanciada. """
		self.dbname = fileName
		# initialize the log settings
		logging.basicConfig(filename='../logs/appConnectionDBClass.log',level=logging.INFO)

	def open_sqlie(self):
		"""	Abre la conexión a la base de datos.
			Returns:
				Retorna la conexión a la base de datos
				en caso de error retorna None.
		"""
		con = None
		try:
			con = sqlite3.connect(self.dbname)
			self.conn = con
		except sqlite3.error as e:
			logging.error("open_sqlie Sqlite error: {0}".format(e))
		except Exception as e:
			logging.error("open_sqlie Exception error: {0}".format(e))
		return self.conn

	def connection_sqlite(self):
		"""	Realiza la conexión a la base de datos si no fue realizada
			y la retorna para su posterior uso.
			Returns:
				sqlite3.connect
		"""
		ret = None
		try:
			ret = self.conn
		except AttributeError:
			ret = self.open_sqlie()			
		return ret

	def __del__(self):
		"""	Finaliza la clase instanciada cerrando la conexión si existe """
		try:
			self.conn.close()
		except AttributeError:
			print('No se abrio la conexión')
			