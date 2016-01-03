import mysql.connector
from mysql.connector import errorcode

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

config = {
  'user': 'root',
  'password': '321', 
  'database': 'db_recomendaciones',
}



def start_mysql_conn(config_dict):
	try:
		cnx = mysql.connector.connect(**config)
		print "connection started."
		cursor = cnx.cursor()
		return cnx, cursor
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print "Something is wrong with your user name or password"
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print "Database does not exist"

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





cnx, cursor = start_mysql_conn(config)

create_db('db_recomendaciones')


cursor.close()
cnx.close()

	


