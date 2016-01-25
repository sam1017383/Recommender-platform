import mysql.connector
from mysql.connector import errorcode
import matplotlib
import matplotlib.pyplot as plt
import re
import time
from datetime import date


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


def exec_query(query):
	try: 
		cursor.execute(query)
		data = cursor.fetchall()
		return data
	except mysql.connector.Error as err:
		print(err)

def print_select(query):
	cursor.execute(query)
	data = cursor.fetchall()
	for each_row in data:
		print each_row


def graph_bars_2groups(group_1, group_2, label_tuple_x, label_1, label_2):
	fig, ax = plt.subplots()
	index = np.arange(len(group_1))
	bar_width = 0.35
	rects1 = plt.bar(index, group_1, bar_width, label=label_1, color='b')
	rects2 = plt.bar(index + bar_width, group_2, bar_width, label=label_2, color='r')
	plt.xticks(index + bar_width, label_tuple_x)
	plt.tight_layout()
	plt.legend()
	plt.show()


def graph_pie_chart(labels, sizes):
	plt.pie(sizes, labels=labels)
	plt.show()


def graph_2D(X,Y, x_label, y_label):
	plt.plot(X, Y, 'or')
	plt.grid(True)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.show()



def plot_genero():
	masculino = exec_query("SELECT COUNT(*) FROM usuarios where Genero='m'")[0][0]
	femenino = exec_query("SELECT COUNT(*) FROM usuarios where Genero='f'")[0][0]
	genero_nd = exec_query("SELECT COUNT(*) FROM usuarios where Genero=''")[0][0]
	
	print "----"
	print "Usuarios hombres: ", masculino
	print "Usuarios mujeres: ", femenino
	print "Usuarios genero no disponible: ", genero_nd

	graph_pie_chart(['Mujeres', 'Hombres', 'No disponible'], [femenino, masculino, genero_nd])

def plot_ciudades(n_top):
	total_usuarios = exec_query("SELECT COUNT(*) FROM usuarios")[0][0]
	ciudades = exec_query("SELECT DISTINCT Ciudad FROM usuarios order by Ciudad")
	list_ciudades = []
	for each_row in ciudades:
		count_city =  exec_query("SELECT COUNT(*) FROM usuarios where Ciudad='" + unicode(each_row[0]).encode('utf8') + "'")[0][0]
		list_ciudades.append((unicode(each_row[0]).encode('utf8'), count_city))

	print "----"
	print "Ciudades distintas: ", len(list_ciudades)
	sorted_cities = sorted(list_ciudades, key=lambda user: user[1], reverse=True)
	labels = []
	sizes = []
	subtot_usuarios = 0
	for each_city in sorted_cities[0:n_top]:
		subtot_usuarios += each_city[1]
		labels.append(re.sub('[^A-Za-z0-9]+', '',each_city[0]))
		sizes.append(each_city[1])
		print each_city[1], " usuarios en ", each_city[0]

	labels.append('Otras ciudades')
	sizes.append(total_usuarios - subtot_usuarios)
	graph_pie_chart(labels, sizes)

def plot_estado_civil():
	casado = exec_query("SELECT COUNT(*) FROM usuarios where Estado_civil='c'")[0][0]
	soltero = exec_query("SELECT COUNT(*) FROM usuarios where Estado_civil='s'")[0][0]
	union_libre = exec_query("SELECT COUNT(*) FROM usuarios where Estado_civil='ul'")[0][0]
	divorciado = exec_query("SELECT COUNT(*) FROM usuarios where Estado_civil='d'")[0][0]
	estado_civil_no_disponible = exec_query("SELECT COUNT(*) FROM usuarios where Estado_civil=''")[0][0]
	
	print "----"
	print "Usuarios casados: ", casado
	print "Usuarios solteros: ", soltero
	print "Usuarios en union libre: ", union_libre
	print "Usuarios divorciados: ", divorciado
	print "Usuarios con estado civil no disponible: ", estado_civil_no_disponible

	graph_pie_chart(['Casados', 'Solteros', 'En union libre', 'Divorciados', 'Estado civil no disponible'], [casado, soltero, union_libre, divorciado, estado_civil_no_disponible])


def plot_hijos():
	cero_hijos = exec_query("SELECT COUNT(*) FROM usuarios where Hijos=0")[0][0]
	un_hijo = exec_query("SELECT COUNT(*) FROM usuarios where Hijos=1")[0][0]
	dos_hijos = exec_query("SELECT COUNT(*) FROM usuarios where Hijos=2")[0][0]
	tres_mas_hijos = exec_query("SELECT COUNT(*) FROM usuarios where Hijos>=3")[0][0]
	hijos_no_disponible = exec_query("SELECT COUNT(*) FROM usuarios where Hijos=''")[0][0]
	
	print "----"
	print "Usuarios sin hijos: ", cero_hijos - hijos_no_disponible
	print "Usuarios con un hijo: ", un_hijo
	print "Usuarios con dos hijos: ", dos_hijos
	print "Usuarios con tres o mas hijos: ", tres_mas_hijos
	print "Usuarios con informacion de hijos no disponible: ", hijos_no_disponible

	graph_pie_chart(['Sin hijos', 'Un hijo', 'Dos hijos', 'Tres o mas hijos', 'Informacion de hijos no disponible'], [cero_hijos - hijos_no_disponible, un_hijo, dos_hijos, tres_mas_hijos, hijos_no_disponible])


def plot_nacimiento(since, until):
	'Filter rows validating dates. "since" and "until" are tuples "(year, month, day)"'
	total_usuarios = exec_query("SELECT COUNT(*) FROM usuarios")[0][0]
	usuarios_nac_valido = exec_query("SELECT COUNT(*) FROM usuarios where Nacimiento <> ''")[0][0]
	print "----"
	print "Usuarios sin fecha de nacimiento: ", total_usuarios - usuarios_nac_valido

	usuarios_nac = exec_query("SELECT Nacimiento FROM usuarios where Nacimiento <> ''")
	years_vector = [0] * 100
	for each_row in usuarios_nac:
		nacimiento =  each_row[0].split('/')
		valids_user_bd = []
		if len(nacimiento) == 3:
			#print {"year": unicode(nacimiento[2]).encode('utf8'), "month": unicode(nacimiento[0]).encode('utf8'),"day": unicode(nacimiento[1]).encode('utf8')}
			valids_user_bd.append({"year": unicode(nacimiento[2]).encode('utf8'), "month": unicode(nacimiento[0]).encode('utf8'),"day": unicode(nacimiento[1]).encode('utf8')})
			years_vector[int(unicode(nacimiento[2]).encode('utf8'))] += 1
	
	graph_2D(range(0,100),years_vector, 'Ano', 'Usuarios')
	

def plot_edad():
	'Filter rows validating dates. "since" and "until" are tuples "(year, month, day)"'
	total_usuarios = exec_query("SELECT COUNT(*) FROM usuarios")[0][0]
	usuarios_nac_valido = exec_query("SELECT COUNT(*) FROM usuarios where Nacimiento <> ''")[0][0]
	print "----"
	print "Usuarios sin fecha de nacimiento: ", total_usuarios - usuarios_nac_valido

	usuarios_nac = exec_query("SELECT Nacimiento FROM usuarios where Nacimiento <> ''")
	edad_vector = [0] * 150
	for each_row in usuarios_nac:
		nacimiento =  each_row[0].split('/')
		valids_user_bd = []
		if len(nacimiento) == 3:
			#print {"year": unicode(nacimiento[2]).encode('utf8'), "month": unicode(nacimiento[0]).encode('utf8'),"day": unicode(nacimiento[1]).encode('utf8')}
			valids_user_bd.append({"year": unicode(nacimiento[2]).encode('utf8'), "month": unicode(nacimiento[0]).encode('utf8'),"day": unicode(nacimiento[1]).encode('utf8')})
			edad = 100 + 16 - int(unicode(nacimiento[2]).encode('utf8'))
			edad_vector[edad] += 1
	graph_2D(range(0,150),edad_vector, 'Ano', 'Usuarios')
	

def plot_coordinates():
	gps_coor = exec_query("SELECT Latitud, Longitud FROM productos")
	latitutes = []
	longitudes = []
	for each_product in gps_coor:
		if re.match('-?[0-9]+\.[0-9]+', each_product[0]) and re.match('-?[0-9]+\.[0-9]+', each_product[1]):
			latitutes.append(float(unicode(each_product[0]).encode('utf8')))
			longitudes.append(float(unicode(each_product[1]).encode('utf8')))
	graph_2D(longitudes, latitutes, 'Longitud', 'Latitud')


def plot_categorias(n_top):
	total_productos = exec_query("SELECT COUNT(*) FROM productos")[0][0]
	categorias = exec_query("SELECT DISTINCT Categoria FROM productos")
	list_categorias = []
	for each_row in categorias:
		count_categorias =  exec_query("SELECT COUNT(*) FROM productos where Categoria='" + unicode(each_row[0]).encode('utf8') + "'")[0][0]
		list_categorias.append((unicode(each_row[0]).encode('utf8'), count_categorias))

	print "----"
	print "Categorias distintas: ", len(list_categorias)
	sorted_categorias = sorted(list_categorias, key=lambda product: product[1], reverse=True)
	labels = []
	sizes = []
	subtot_productos = 0
	for each_cat in sorted_categorias[0:n_top]:
		subtot_productos += each_cat[1]
		labels.append(re.sub('[^A-Za-z0-9]+', '',each_cat[0]))
		sizes.append(each_cat[1])
		print each_cat[1], " productos tipo ", each_cat[0]

	labels.append('Otras categorias')
	sizes.append(total_productos - subtot_productos)
	graph_pie_chart(labels, sizes)


cnx, cursor = start_mysql_conn(config)
cursor.execute("use db_recomendaciones")

def plot_municipios(n_top):
	total_productos = exec_query("SELECT COUNT(*) FROM productos")[0][0]
	municipios = exec_query("SELECT DISTINCT Municipio FROM productos")
	list_municipios = []
	for each_row in municipios:
		count_municipio =  exec_query("SELECT COUNT(*) FROM productos where Municipio='" + unicode(each_row[0]).encode('utf8') + "'")[0][0]
		list_municipios.append((unicode(each_row[0]).encode('utf8'), count_municipio))

	print "----"
	print "Municipios distintas: ", len(list_municipios)
	sorted_municipios = sorted(list_municipios, key=lambda product: product[1], reverse=True)
	labels = []
	sizes = []
	subtot_productos = 0
	for each_cat in sorted_municipios[0:n_top]:
		subtot_productos += each_cat[1]
		labels.append(re.sub('[^A-Za-z0-9]+', '',each_cat[0]))
		sizes.append(each_cat[1])
		print each_cat[1], " productos tipo ", each_cat[0]

	labels.append('Otros municipios')
	sizes.append(total_productos - subtot_productos)
	graph_pie_chart(labels, sizes)


cnx, cursor = start_mysql_conn(config)
cursor.execute("use db_recomendaciones")

print_select("describe usuarios")
# plot_genero()
plot_ciudades(20)
# plot_estado_civil()
# plot_hijos()
# plot_nacimiento((1900,1,1), (2016,1,1))
# plot_edad()

# plot_coordinates()
#plot_categorias(90)
#plot_municipios(50)

