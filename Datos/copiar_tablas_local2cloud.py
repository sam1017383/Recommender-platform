# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mysql.connector
from mysql.connector import errorcode
import MySQLdb
import csv
import re

# To run the first time and create a database:
# Run the mysql sever. 
# In the terminal type: alias mysql=/usr/local/mysql/bin/mysql
# Log in with default credencials: mysql --user=root --password='root_default_pass'
# Update password: ALTER USER 'root'@'localhost' IDENTIFIED BY '321';
# Create new user: CREATE USER 'sam'@'localhost' IDENTIFIED BY '321';
# CREATE DATABASE db_recomendaciones;



def get_mysql_conn_cursor_cloud():

	cnx = MySQLdb.connect(host='173.194.80.66', port=3306, user='admin', passwd='admin')
	print "Conexion a cloud SQL iniciada"
	cursor = cnx.cursor()
	return cnx, cursor



def get_mysql_conn_cursor_local():

	config = {
	'user': 'root',
	'password': '123', 
	'database': 'db_recomendaciones',
	}
	try:
		cnx = mysql.connector.connect(**config)
		print "Conexion a mySQL local iniciada"
		cursor = cnx.cursor()
		return cnx, cursor
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print "Usuario o contrasena no validos"
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print "No se encuentra la base de datos"

		else:
			print(err)


def copy_users_local2cloud(cursor_local, cursor_cloud, table_name, id_min, id_max):
	print "imprimiendo consulta:"
	select = "select * from "+table_name+" where id>=" + str(id_min) + " and id<=" + str(id_max)
	cursor_local.execute(select)
	datos_local = cursor_local.fetchall()
	for cada_registro in datos_local:
		#print "cada algo:", cada_registro
		CP = cada_registro[0]
		Genero = cada_registro[1]
		Apellido_p = cada_registro[2]
		Apellido_m = cada_registro[3]
		Ciudad = cada_registro[4]
		Hijos = cada_registro[5]
		_id = cada_registro[6]
		Nombre = cada_registro[7]
		Estado_civil = cada_registro[8]
		Contacto = cada_registro[9]
		Nacimiento = cada_registro[10]


		fields = "CP,Genero,Apellido_p,Apellido_m,Ciudad,Hijos,id,Nombre,Estado_civil,Contacto,Nacimiento"
		values = "'"+CP+"','"+Genero+"','"+Apellido_p+"','"+Apellido_m+"','"+Ciudad+"','"+Hijos+"','"+str(_id)+"','"+Nombre+"','"+Estado_civil+"','"+Contacto+"','"+Nacimiento+"'"
		stmt_insert = "INSERT INTO " + table_name + " (" + fields + ") VALUES (" + values + ")"
		#print "Sentencia insert: ", stmt_insert.encode("utf8")
		cursor_cloud.execute(stmt_insert.encode("utf8"))


def copy_product_local2cloud(cursor_local, cursor_cloud, id_min, id_max):
	print "imprimiendo consulta:"
	select = "select * from product where id>=" + str(id_min) + " and id<=" + str(id_max)
	cursor_local.execute(select)
	datos_local = cursor_local.fetchall()
	for cada_registro in datos_local:
		#print "cada algo:", cada_registro
		Categoria = cada_registro[0]
		Latitud = cada_registro[1]
		Contacto = cada_registro[2]
		Colonia = cada_registro[3]
		Direccion = cada_registro[4]
		Alias = cada_registro[5]
		Longitud = cada_registro[6]
		Nombre = cada_registro[7]
		Descripcion = cada_registro[8]
		_id = cada_registro[9]
		CP = cada_registro[10]
		Estado = cada_registro[11]
		Municipio = cada_registro[12]
		Calificable = cada_registro[13]


		fields = "Categoria, Latitud, Contacto, Colonia, Direccion, Alias, Longitud, Nombre, Descripcion, id, CP, Estado, Municipio, Calificable"
		values = "'"+Categoria+"','"+Latitud+"','"+Contacto+"','"+Colonia+"','"+Direccion+"','"+Alias+"','"+Longitud+"','"+Nombre+"','"+Descripcion+"','"+str(_id)+"','"+CP+"','"+Estado+"','"+Municipio+"','"+str(Calificable)+"'"
		stmt_insert = "INSERT INTO product (" + fields + ") VALUES (" + values + ")"
		#print "Sentencia insert: ", stmt_insert.encode("utf8")
		cursor_cloud.execute(stmt_insert.encode("utf8"))





def copy_product_extras_local2cloud(cursor_local, cursor_cloud, id_min, id_max):
	print "imprimiendo consulta:"
	select = "select * from product_extras where id>=" + str(id_min) + " and id<=" + str(id_max)
	cursor_local.execute(select)
	datos_local = cursor_local.fetchall()
	for cada_registro in datos_local:
		#print "cada algo:", cada_registro
		Imagen_fuente = cada_registro[0]
		Calificacion = cada_registro[1]
		Precio = cada_registro[2]
		Descuento = cada_registro[3]
		_id = cada_registro[4]
		Fecha = cada_registro[5]
		Product_id = cada_registro[6]

		fields = "Imagen_fuente, Calificacion, Precio, Descuento, id, Fecha, Product_id"
		values = "'"+Imagen_fuente+"','"+str(Calificacion)+"','"+str(Precio)+"','"+str(Descuento)+"','"+str(_id)+"','"+str(Fecha)+"','"+str(Product_id)+"'"
		stmt_insert = "INSERT INTO product_extras (" + fields + ") VALUES (" + values + ")"
		#print "Sentencia insert: ", stmt_insert.encode("utf8")
		cursor_cloud.execute(stmt_insert.encode("utf8"))


def copy_auth_user_local2cloud(cursor_local, cursor_cloud, id_min, id_max):
	print "imprimiendo consulta:"
	select = "select * from auth_user where id>=" + str(id_min) + " and id<=" + str(id_max)
	cursor_local.execute(select)
	datos_local = cursor_local.fetchall()
	for cada_registro in datos_local:
		#print "cada algo:", cada_registro
		_id = cada_registro[0]
		password = cada_registro[1]
		last_login = cada_registro[2]
		is_superuser = cada_registro[3]
		username = cada_registro[4]
		first_name = cada_registro[5]
		last_name = cada_registro[6]
		email = cada_registro[7]
		is_staff = cada_registro[8]
		is_active = cada_registro[9]
		date_joined = cada_registro[10]

		fields = "id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined"
		values = "'"+str(_id)+"','"+password+"','"+str(last_login)+"','"+str(is_superuser)+"','"+username+"','"+first_name+"','"+last_name+"','"+email+"','"+str(is_staff)+"','"+str(is_active)+"','"+str(date_joined)+"'"
		stmt_insert = "INSERT INTO auth_user (" + fields + ") VALUES (" + values + ")"
		#print "Sentencia insert: ", stmt_insert.encode("utf8")
		cursor_cloud.execute(stmt_insert)



def crea_tabla_config(table_name, column_list, type_list):
	'load a list of dictionaries containing data from csv file to a table'

	#Al crear la tabla, el campo con nombre id_xxx se asigna como entero y llave primaria
	#el resto de campos se asignan como cadena
	stmt = "CREATE TABLE " + table_name + " ( id int, "
	for each_field in range(0, len(column_list)):
		stmt += column_list[each_field] + " " + type_list[each_field] + ", "
	
	stmt += 'PRIMARY KEY(id))'
	print "Sentencia para creacion de tabla: ", stmt
	cursor_cloud.execute(stmt)
	cursor_cloud.execute("show tables")
	print "Tablas en la base de datos: ", cursor_cloud.fetchall()
	cursor_cloud.execute("describe " + table_name)
	print "descripcion de la tabla " + table_name + ": ", cursor_cloud.fetchall()

	
	
	# Guarda de persistentemente
	# cnx.commit()



	
	#cursor.execute("DROP TABLE " + table_name)''
	#cursor.execute("show tables")
	#print "show without new table: ",cursor.fetchall()
	
	

def cargar_recomendadores_config(tabla, title_list, algorithm_list, longitud_max_list, param_list):
	print "imprimiendo consulta:"
	for cada_registro in range(0,len(title_list)):
		
		titulo = title_list[cada_registro]
		algoritmo = algorithm_list[cada_registro]
		long_max = longitud_max_list[cada_registro]
		param = param_list[cada_registro]

		fields = "titulo_interfaz, algoritmo_recomendador, longitud_max, param"
		values = "'"+titulo+"','"+algoritmo+"','"+long_max+"','"+param+"'"
		stmt_insert = "INSERT INTO "+tabla+" (" + fields + ") VALUES (" + values + ")"
		print "Sentencia insert: ", stmt_insert.encode("utf8")
		cursor_cloud.execute(stmt_insert)


def print_select(query):
	cursor.execute(query)
	data = cursor.fetchall()
	for each_row in data:
		print each_row




cnx_local, cursor_local = get_mysql_conn_cursor_local()
cnx_cloud, cursor_cloud = get_mysql_conn_cursor_cloud()

cursor_local.execute("use recommender")
cursor_cloud.execute("use xtidb")


#copy_users_local2cloud(cursor_local, cursor_cloud,"users", 20001, 226185)
#copy_product_local2cloud(cursor_local, cursor_cloud, 101, 7049)
#copy_product_extras_local2cloud(cursor_local, cursor_cloud, 101, 7049)
#copy_auth_user_local2cloud(cursor_local, cursor_cloud, 101, 226185)

#crea_tabla_config("recomendaciones_config", ["titulo", "algoritmo", "long_max", "parametro"], ["varchar(255)", "varchar(255)", "int", "int"])

titulos = ["Productos que has calificado", 
			"Lo más comentado en tu ciudad",
			"Recomendaciones a tu pefil",
			"Nuevas alianzas X-ti",
			"Usuarios como tú recomiendan",
			"Productos similares a los que te han gustado",
			"Usuarios con gustos similares les han gustado",
			"Productos interesantes para tí",
			]

algos = ["calificados", 
			"comentados_ciudad",
			"reglas_perfil",
			"nuevos",
			"usuario_similar_demografico",
			"productos_similares_gustado",
			"filtrado_colaborativo",
			"hibrido",
			]
longs = ["15", 
			"10",
			"15",
			"10",
			"15",
			"10",
			"15",
			"10",
			]
params = ["0", 
			"90",
			"0",
			"90",
			"0",
			"0",
			"0",
			"0",
			]


# cargar_recomendadores_config("listas_recomendadores_config", titulos, algos, longs, params)
# Guarda de persistentemente
cnx_cloud.commit()


cnx_local.close()
cnx_cloud.close()

	