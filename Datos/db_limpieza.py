# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode
import csv
import re



# To run the first time and create a database:
# Run the mysql sever. 
# In the terminal type: alias mysql=/usr/local/mysql/bin/mysql
# Log in with default credencials: mysql --user=root --password='root_default_pass'
# Update password: ALTER USER 'root'@'localhost' IDENTIFIED BY '321';
# Create new user: CREATE USER 'sam'@'localhost' IDENTIFIED BY '321';
# CREATE DATABASE db_recomendaciones;


# 
config = {
  'user': 'root',
  'password': '123', 
  'database': 'db_recomendaciones',
}



def start_mysql_conn(config_dict):
	try:
		cnx = mysql.connector.connect(**config)
		print "Conexion iniciada"
		cursor = cnx.cursor()
		return cnx, cursor
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print "Usuario o contrasena no validos"
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print "No se encuentra la base de datos"

		else:
			print(err)




def limpiar_rango(tabla, campo_id, campo, minimo, maximo, defecto):
	query = "select " + campo_id + ", " + campo + " from " + tabla + ";"
	cursor.execute(query)
	data = cursor.fetchall()
	for cada_elemento in data:
		
		if cada_elemento[1] != "":
			cadena_valor = re.sub(" ", "", cada_elemento[1])
			cadena_valor = re.sub("\D", "0", cadena_valor)
			valor = int(cadena_valor)
			id_registro = int(cada_elemento[0])
			#update
			if valor < minimo or valor > maximo:
				query = "update " + tabla + " set " + campo + " = " + str(defecto) + " where " + campo_id + " = " + str(id_registro) + ";"
				print query
				cursor.execute(query)
		else:
			id_registro = int(cada_elemento[0])
			#update
			query = "update "+ tabla + " set " + campo + " = " + str(defecto) + " where " + campo_id + " = " + str(id_registro) + ";"
			print query
			cursor.execute(query)

	# Guarda de persistentemente
	cnx.commit()

def limpiar_rango_float(tabla, campo_id, campo, minimo, maximo, defecto):
	query = "select " + campo_id + ", " + campo + " from " + tabla + ";"
	cursor.execute(query)
	data = cursor.fetchall()
	for cada_elemento in data:
		
		if cada_elemento[1] != "" and cada_elemento[1] != "FALTA":
			cadena_valor = re.sub(" ", "", cada_elemento[1])
			cadena_valor = re.sub("--", "-", cada_elemento[1])
			valor = float(cadena_valor)
			id_registro = int(cada_elemento[0])
			#print "elemento ", id_registro , " no nulo: ", valor
			#update
			if valor < minimo or valor > maximo:
				query = "update " + tabla + " set " + campo + " = " + str(defecto) + " where " + campo_id + " = " + str(id_registro) + ";"
				print query
				cursor.execute(query)
		else:
			id_registro = int(cada_elemento[0])
			#update
			query = "update "+ tabla + " set " + campo + " = " + str(defecto) + " where " + campo_id + " = " + str(id_registro) + ";"
			print query
			cursor.execute(query)

	# Guarda de persistentemente
	cnx.commit()

		
def limpiar_opciones(tabla, campo_id, campo, opciones, defecto):
	query = "select " + campo_id + ", " + campo + " from " + tabla + ";"
	cursor.execute(query)
	data = cursor.fetchall()
	for cada_elemento in data:
		if cada_elemento[1] not in opciones:
			#update
			id_registro = int(cada_elemento[0])
			query = "update "+ tabla + " set " + campo + " = '" + defecto + "' where " + campo_id + " = " + str(id_registro) + ";"
			print query
			cursor.execute(query)
	# Guarda de persistentemente
	cnx.commit()
	

def limpiar_texto(tabla, campo_id, campo):
	query = "select " + campo_id + ", " + campo + " from " + tabla + ";"
	cursor.execute(query)
	data = cursor.fetchall()
	for cada_elemento in data:
		id_registro = int(cada_elemento[0])
		texto = cada_elemento[1]
		texto = texto.encode("utf-8")
		print "id: ", str(id_registro), "  texto: ", texto
		texto = re.sub("\.", "", texto)
		texto = re.sub("\,", "", texto)
		texto = re.sub("^ ", "", texto)
		texto = re.sub("  ", " ", texto)

		texto = re.sub("Áƒâ€˜", "Ñ", texto)
		texto = re.sub("ÃƒÆ’Ã‚Â", "Á", texto)
		texto = re.sub("Â Â", "A", texto)
		
		texto = re.sub("ÃƒÆ’Ã¢â‚¬Â°", "É", texto)
		texto = re.sub("Ãƒâ€°", "É", texto)
		texto = re.sub("ÁƒÆ’Á¢â‚¬Ëœ", "Ñ", texto)
		texto = re.sub("Áƒâ€˜", "Ñ", texto)
		
		
		texto = re.sub("TÃ", "TÍ", texto)
		texto = re.sub("TÍƒÂ", "TÍ", texto)
		texto = re.sub("ÃAN", "IAN", texto)
		texto = re.sub("VÃC", "VIC", texto)
		texto = re.sub("ÁƒÂ", "Í", texto)

		texto = re.sub("Ãƒâ€œ", "Ó", texto)
		
		texto = re.sub("ÃƒÆ’Ã…Â¡", "Ú", texto)
		texto = re.sub("ÃƒÅ¡", "Ú", texto)
		texto = re.sub("Ãš", "Ú", texto)

		texto = re.sub("Ã“", "Ó", texto)
		texto = re.sub("Ã‘", "Ñ", texto)
		texto = re.sub("Ã‰", "E", texto)
		texto = re.sub("Ã©", "e", texto)

		texto = re.sub("Ã", "Á", texto)
		

		texto = re.sub("SIN NOMBRE", "", texto)
		texto = re.sub("INGRESA TU NOMBRE", "", texto)
		texto = re.sub("INGRESA TU APELLIDO MATERNO", "", texto)
		texto = re.sub("INGRESA TU APELLIDO PATERNO", "", texto)

		texto = re.sub("DF", "DISTRITO FEDERAL", texto)
		texto = re.sub("MEXICO DF", "DISTRITO FEDERAL", texto)
		texto = re.sub("CD MEXICO", "DISTRITO FEDERAL", texto)
		texto = re.sub("CIUDAD DE MEXICO", "DISTRITO FEDERAL", texto)
		texto = re.sub("MÉXICO DF", "DISTRITO FEDERAL", texto)
		texto = re.sub("MÉXICO DISTRITO FEDERAL", "DISTRITO FEDERAL", texto)
		texto = re.sub("MEXICO DISTRITO FEDERAL", "DISTRITO FEDERAL", texto)
		texto = re.sub("CIUDAD DE MEXICO", "DISTRITO FEDERAL", texto)
		texto = re.sub("MEXICO CITY", "DISTRITO FEDERAL", texto)

		texto = re.sub("EDO DE MEXICO", "ESTADO DE MEXICO", texto)
		texto = re.sub("EDO MEX", "ESTADO DE MEXICO", texto)

		#update
		query = "update "+ tabla + " set " + campo + " = '" + texto + "' where " + campo_id + " = " + str(id_registro) + ";"
		#print query
		cursor.execute(query)
	# Guarda de persistentemente
	cnx.commit()

def limpiar_correo(tabla, campo_id, campo):
	correos_unicos = []
	query = "select " + campo_id + ", " + campo + " from " + tabla + ";"
	cursor.execute(query)
	data = cursor.fetchall()

	for cada_elemento in data:
		id_registro = int(cada_elemento[0])
		texto = cada_elemento[1]
		texto = texto.encode("utf-8")
		if texto in correos_unicos:
			query = "update "+ tabla + " set " + campo + " = '"  + "' where " + campo_id + " = " + str(id_registro) + ";"
			cursor.execute(query)
		
		elif not re.match('.+\@.+', texto):
			#update
			print "El usuario ", cada_elemento[0], "  con correo: ", texto, " tiene pecs"
			query = "update "+ tabla + " set " + campo + " = '"  + "' where " + campo_id + " = " + str(id_registro) + ";"
			cursor.execute(query)
		else:
			correos_unicos.append(texto)

	# Guarda de persistentemente
	cnx.commit()


def remover_nulos(tabla, campo_id, campo):
	query = "select " + campo_id + ", " + campo + " from " + tabla + ";"
	cursor.execute(query)
	data = cursor.fetchall()
	for cada_elemento in data:
		id_registro = int(cada_elemento[0])
		if  cada_elemento[1] == "":
			print "El usuario ", cada_elemento[0], " tiene campo vacio"
			#update
			query = "delete from "+ tabla + " where " + campo_id + " = " + str(id_registro) + ";"
			print query
			cursor.execute(query)
	# Guarda de persistentemente
	cnx.commit()

def insertar_extras(producto_id, imagen_url, calificacion, precio, descuento):
	query = "INSERT INTO product_extras (Fecha, Imagen_fuente, Calificacion, Precio, Descuento, Product_id) " 
	query += "VALUES(NOW(), " + imagen_url + ", " + calificacion + ", " + precio + ", " + descuento + ", " + producto_id + ");"
	print "QUERY: ", query
	cursor.execute(query)
	# Guarda de persistentemente
	cnx.commit()

def cargar_extras_default():
	query = "select id from product;"
	cursor.execute(query)
	productos_id = cursor.fetchall()
	for cada_id in productos_id:
		insertar_extras(str(cada_id[0]), "'/static/image/doctor_general.jpg'", '3.5', '99.9', '20.5')

def actualizar_imagen_por_categoria(categoria, nueva_imagen):
	query = "select id from product where Categoria = '" + categoria + "';"
	cursor.execute(query)
	productos_id = cursor.fetchall()
	print "cambios a realizar: ", len(productos_id)
	for cada_id in productos_id:
		query = "update product_extras SET Imagen_fuente= '" + nueva_imagen +"' WHERE Product_id=" + str(cada_id[0]) + ";"
		cursor.execute(query)
	
	cnx.commit()

def actualizar_imagen_por_nombre_like(nombre, nueva_imagen):
	query = "select id from product where Nombre LIKE '%" + nombre + "%';"
	cursor.execute(query)
	productos_id = cursor.fetchall()
	print "cambios a realizar: ", len(productos_id)
	for cada_id in productos_id:
		query = "update product_extras SET Imagen_fuente= '" + nueva_imagen +"' WHERE Product_id=" + str(cada_id[0]) + ";"
		cursor.execute(query)
	
	cnx.commit()
	



cnx, cursor = start_mysql_conn(config)
cursor.execute("use recommender")
cursor.execute("show tables")
print cursor.fetchall()

# # limpiar base de datos de usuario
# limpiar_rango("usuarios", "id_usuario", "CP", 1, 99000, 0)
# limpiar_rango("usuarios", "id_usuario", "Hijos", 0, 4, 0)
# limpiar_opciones("usuarios", "id_usuario", "Genero", ["m", "f"], "n")
# limpiar_opciones("usuarios", "id_usuario", "Estado_civil", ["c", "s", "ul", "d"], "s")
# limpiar_texto("usuarios", "id_usuario", "Nombre")
# limpiar_texto("usuarios", "id_usuario", "Apellido_m")
# limpiar_texto("usuarios", "id_usuario", "Apellido_p")
# limpiar_texto("usuarios", "id_usuario", "Ciudad")
# limpiar_correo("usuarios", "id_usuario", "Contacto")
# remover_nulos("usuarios", "id_usuario", "Contacto")

# #limpiar_rango("productos", "id_producto", "CP", 1, 99000, 0)
# limpiar_rango_float("productos", "id_producto", "Latitud", 14.0, 33.0, 0)
# limpiar_rango_float("productos", "id_producto", "Longitud", -117.0, -85.0, 0)
# limpiar_texto("productos", "id_producto", "Categoria")
# limpiar_texto("productos", "id_producto", "Colonia")
# limpiar_texto("productos", "id_producto", "Alias")
# limpiar_texto("productos", "id_producto", "Nombre")
# limpiar_texto("productos", "id_producto", "Descripcion")
# limpiar_texto("productos", "id_producto", "Estado")
# limpiar_texto("productos", "id_producto", "Municipio")

#cargar_extras_default()

actualizar_imagen_por_nombre_like("CHOPO", "/static/image/laboratorios_chopo.png")
cnx.close()

	

