#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xmlrpc.server
import os.path
import logging

# initialize the log settings
logging.basicConfig(filename='logs/appDocumentoWS.log',level=logging.INFO)

url = 'http://192.168.0.32:8000/usuario'
cliente = xmlrpc.client.ServerProxy(url)

if __name__ == "__main__":
	strHTML = "<!DOCTYPE html><html><head><title>{0}</title>{1}</head><body style='background-color:indigo;'>{2}</body></html>"
	strDiv = "<div><h2>{0}</h2><div><p>{1}</p><p>{2}</p></div></div>"
	strBody = "<h1 style='text-align:center;color:floralwhite;''>Documento wsAccionesDeUsuario</h1><ol style='display:block;background-color:green;padding:20px;border:10px;'>"
	lstMetodos = cliente.system.listMethods()
	for metodo in lstMetodos:
		if 'system.' not in metodo:
			strBody +="<li style='margin-left: 20px;color:white'>{0}</li>".format(metodo)
	strBody += "</ol><dl style='background-color:lightgrey;padding-bottom:5px'>"
	for metodo in lstMetodos:
		if 'system.' not in metodo:
			strBody +="<dt style='background-color:skyblue;padding:5px;padding-left:15px;'><strong>{0}</strong></dt><dd><div><pre><p>{1}</p><p>{2}</p></div></pre></dd>".format(metodo,cliente.system.methodHelp(metodo),"<i>methodSignature:</i> {0}".format(cliente.system.methodSignature(metodo)))
	strBody += "</dl>"
	retorno = strHTML.format('wsAccionesDeUsuario', '', strBody)

	# print(retorno)
	try:
		strPath = os.path.realpath('ayuda')
		strNombre = os.path.join(strPath, 'wsAccionesUsuarioDoc.html')

		if os.path.exists(strNombre):
			os.remove(strNombre)
		
		docAyuda = open(strNombre, "w")
		docAyuda.write(retorno)
		docAyuda.close()
	except Exception as e:
		logging.error('Error occurred {0}'.format(e))