#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xmlrpc.server

url = 'http://192.168.0.32:8000/usuario'
cliente = xmlrpc.client.ServerProxy(url)

if __name__ == "__main__":
	print("agregarUsuario 0 = {0}".format(cliente.agregarUsuario('svasilovski', '7b65hf39cc42')))
	print("agregarUsuario 0 = {0}".format(cliente.agregarUsuario('jperez', 'perez jose')))
	print("agregarUsuario 0 = {0}".format(cliente.agregarUsuario('lroderiguez', 'laura roderiguez')))
	print("bloquearDesbloquearUsuario 0 = {0}\n".format(cliente.bloquearDesbloquearUsuario('jperez', 0)))
	print("actualizarUsuario 0 = {0}".format(cliente.actualizarUsuario('svasilovski', '7b65hf39cc42', 'samuel vasilovski', 'samuel vasilovski')))
	print("eliminarUsuario 0 = {0}".format(cliente.eliminarUsuario('lroderiguez', 'laura roderiguez')))
	
	lstUser = cliente.listarUsuarios()
	for u in lstUser:
		print('lstUser\t{0}'.format(u))

	validoUno = cliente.validarUsuario("svasilovski", "7b65hf39cc42")
	print("validarUsuario 4 = {0}".format(validoUno))
	validoDos=cliente.validarUsuario("svasilovski", "samuel vasilovski")
	print("validarUsuario 3 = {0}".format(validoDos))