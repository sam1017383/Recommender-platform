import mysql.connector
from mysql.connector import errorcode

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



def print_select(query):
	cursor.execute(query)
	data = cursor.fetchall()
	for each_row in data:
		print each_row


cnx, cursor = start_mysql_conn(config)
cursor.execute("use db_recomendaciones")

print_select("show tables")
