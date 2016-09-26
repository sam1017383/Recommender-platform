# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode
import MySQLdb
import csv
import re
import random

# To run the first time and create a database:
# Run the mysql sever. 
# In the terminal type: alias mysql=/usr/local/mysql/bin/mysql
# Log in with default credencials: mysql --user=root --password='root_default_pass'
# Update password: ALTER USER 'root'@'localhost' IDENTIFIED BY '321';
# Create new user: CREATE USER 'sam'@'localhost' IDENTIFIED BY '321';
# CREATE DATABASE db_recomendaciones;


comentarios_predefinidos = [
	"esto es nulo",
	"Este producto es pésimo",
	"El producto es muy deficiente, no recomendable",
	"El lugar no es bueno, mejor evítalo",
	"Buen servicio! recomendable!",
	"Excelente! Magnífico!"
	
]



def start_mysql_conn_cloud():

	cnx = MySQLdb.connect(host='173.194.80.66', port=3306, user='admin', passwd='admin')
	print "Conexion iniciada"
	cursor = cnx.cursor()
	return cnx, cursor



# 
config = {
  'user': 'root',
  'password': '123', 
  'database': 'xti',
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



def cargar_comentarios_azar(cursor, productos, usuarios, calificaciones_por_usuario):

	for cada_usuario in  usuarios:
		for i in range(0, calificaciones_por_usuario):
			producto_calificar = productos[random.randint(0, len(productos)-1)]
			
			fields = "calificacion_producto, comentario, product_id, users_id"
			opcion = random.randint(1, 5)
			values =  "'" + str(opcion) + "', '" + comentarios_predefinidos[opcion] + "','" + str(producto_calificar[9]) + ", '" + str(cada_usuario[6]) + "'"
			stmt_insert = "INSERT INTO calificaciones (" + fields + ") VALUES (" + values + ")"
			print "Sentencia insert: ", stmt_insert
			cursor.execute(stmt_insert)



def load_dicts_to_sql_comments(table_name, data_dict):
	'load a list of dictionaries containing data from csv file to a table'

	#Al crear la tabla, el campo con nombre id_xxx se asigna como entero y llave primaria
	#el resto de campos se asignan como cadena
	stmt = "CREATE TABLE " + table_name + " (id int(11), calificacion_producto int(11), "
	stmt +=	"comentario longtext, fecha date, hora time, productx_id int(11), userx_id int(11), "
	stmt += 'PRIMARY KEY(id))'
	print "Sentencia para creacion de tabla: ", stmt
	cursor.execute(stmt)
	cursor.execute("show tables")
	print "Tablas en la base de datos: ", cursor.fetchall()
	cursor.execute("describe " + table_name)
	print "descripcion de la tabla " + table_name + ": ", cursor.fetchall()

	# Itera la lista de diccionarios con llaves iguales a las columnas de la tabla
	# insertando cada valor en su correspondiente columna
	
	for each_row in data_dict:
		fields = ""
		values = ""
		for each_column in data_dict[0].keys():
			fields += str(each_column) + ", "
			texto = re.sub('"', "'", each_row[str(each_column)])
			values += '"' + texto + '", '


		fields = fields[0:len(fields)-2]
		values = values[0:len(values)-2]
		stmt_insert = "INSERT INTO " + table_name + "(" + fields + ") VALUES (" + values + ")"
		print "Sentencia insert: ", stmt_insert
		cursor.execute(stmt_insert)
		
	
	#cursor.execute("DROP TABLE " + table_name)''
	#cursor.execute("show tables")
	#print "show without new table: ",cursor.fetchall()
	
	# Guarda de persistentemente
	cnx.commit()




# se insertan 10,000 comentarios de 1000 usuarios sobre 1000 productos, 10 por usuario
cnx, cursor = start_mysql_conn(config)
cursor.execute("use xti")

# se colectan 1000 usuarios al azar
cursor.execute("select * from v_users order by rand() limit 1000")
usuarios = cursor.fetchall()
print "USUARIOS: _______"
for each_row in usuarios:
		print each_row

# se colectan 1000 productos al azar
cursor.execute("select * from product order by rand() limit 1000")
productos  = cursor.fetchall()
print "PRODUCTOS: _______"
for each_row in productos:
		print each_row


cargar_comentarios_azar(cursor, productos, usuarios, 10)




cnx.close()
