# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode
import csv
import re


config_template = {
  'user': 'root',
  'password': 'sBO62MYytL+K',
  'host': '127.0.0.1',
  'database': 'employees',
  'raise_on_warnings': True,
}


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
  'password': '321', 
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


def create_db(name):
	try:
		cursor.execute(
				"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name))
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_BAD_DB_ERROR:
			try:
				cursor.execute(
				"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name))
				print "Data base created."
			except mysql.connector.Error as err:
				print "Failed creating database: {}".format(err)
	else:
		print(err)


def create_table(name, fields):
	stmt = "CREATE TABLE " + name + " (dept_no char(4) NOT NULL, dept_name varchar(40) NOT NULL, PRIMARY KEY (dept_no)) ENGINE=InnoDB" 
	cursor.execute(stmt)
	cursor.execute("show tables")
	print cursor.fetchall()


def load_csv(csv_file):
	'load csv file to list of dictionaries'
	try:
		data = []
		raw_data = csv.DictReader(open(csv_file))
		print "Data loaded!" 
		for each_row in raw_data:
			data.append(each_row)
		return data
	except ValueError:
		print "Error: " + ValueError	
		return []

def load_dicts_to_sql_table(table_name, data_dict):
	'load a list of dictionaries containing data from csv file to a table'

	#Al crear la tabla, el campo con nombre id_xxx se asigna como entero y llave primaria
	#el resto de campos se asignan como cadena
	stmt = "CREATE TABLE " + table_name + " ("
	for each_field in data_dict[0]:
		print each_field
		if re.match('id\_\w', each_field):
			field_type = 'int'
			primary_key = each_field
		else:
			field_type = 'varchar(255)'
		stmt += each_field + " " + field_type + ", "
	stmt += 'PRIMARY KEY('+ primary_key +'))'
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
			fields += each_column + ", "
			values += "'" + each_row[each_column] + "', "
		fields = fields[0:len(fields)-2]
		values = values[0:len(values)-2]
		stmt_insert = "INSERT INTO " + table_name + "(" + fields + ") VALUES (" + values + ")"
		#print "Sentencia: ", stmt_insert
		cursor.execute(stmt_insert)
		
	
	#cursor.execute("DROP TABLE " + table_name)
	#cursor.execute("show tables")
	#print "show without new table: ",cursor.fetchall()
	
	# Guarda de persistentemente
	cnx.commit()





def load_dicts_to_sql_comments(table_name, data_dict):
	'load a list of dictionaries containing data from csv file to a table'

	#Al crear la tabla, el campo con nombre id_xxx se asigna como entero y llave primaria
	#el resto de campos se asignan como cadena
	stmt = "CREATE TABLE " + table_name + " (id int(11), calificacion_producto int(11), "
	stmt +=	"comentario longtext, fecha date, hora time, productx_id int(11), userx_id int(11), "
	stmt += 'PRIMARY KEY(id))'
	exitprint "Sentencia para creacion de tabla: ", stmt
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
			fields += each_column + ", "
			texto = re.sub('"', "'", each_row[each_column])
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




def print_select(query):
	cursor.execute(query)
	data = cursor.fetchall()
	for each_row in data:
		print each_row




def test():
	create_table('lol', [['field', 'type']])




cnx, cursor = start_mysql_conn(config)
cursor.execute("use xti_recomendaciones")
cursor.execute("show tables")
print cursor.fetchall()

#data_dict_usuarios = load_csv('usuarios.csv')
#data_dict_productos = load_csv('productos.csv')
data_dict_comentarios = load_csv('comentarios.csv')

#load_dicts_to_sql_table('usuarios', data_dict_usuarios)
#load_dicts_to_sql_table('productos', data_dict_productos)
load_dicts_to_sql_comments('comentarios', data_di ct_comentarios)

print "USUARIOS: _______"
#print_select("select * from usuarios where id_usuario<10")

print "PRODUCTOS: _______"
#print_select("select * from productos where id_producto<10")



cnx.close()

	


