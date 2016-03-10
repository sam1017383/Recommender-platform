import MySQLdb

config = {
  'user': 'root',
  'password': '123', 
  'database': 'db_recomendaciones',
}


def start_mysql_conn(config_dict):
	
	cnx = MySQLdb.connect(host='173.194.80.66', port=3306, user='admin', passwd='admin')
	print "Conexion iniciada"
	cursor = cnx.cursor()
	return cnx, cursor
	


cnx, cursor = start_mysql_conn(config)
cursor.execute("show databases")
cursor.execute("use prueba_db")
cursor.execute("CREATE TABLE Persons(PersonID int,LastName varchar(255),FirstName varchar(255),Address varchar(255),City varchar(255))")

cursor.execute("DESCRIBE Persons")

print cursor.fetchall()
cnx.close()