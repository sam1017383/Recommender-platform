
import sys
sys.path.insert(0, '/usr/local/lib/python2.7/site-packages')
import pymssql  
import csv


class data_manager():

	#server='192.168.0.172'
	server='go4it.supportdesk.com.mx'
	user='userAvaluos'
	password='M3x1c087'
	database='ExtracAvaluo'




	select_fields = [ 	
							"LONGITUD",
							"LATITUD",
							"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE",
							"CLAVE_MUNICIPIO_UBICACION_INMUEBLE",
							"CAT_TIPO_INMUEBLE",
							"CVE_NIVEL_INFRAESTR_URBANA",
							"CVE_NIVEL_EQUIPAMIENTO_URBANO",
							"CVE_CLASE_INMUEBLE",
							"CVE_USO_CONSTRUCCION",
							"FACTOR_RESULTANTE_PRIVATIVAS",
							"FACTOR_EDAD_PRIVATIVAS",
							"FACTOR_CONSERVACION_PRIVATIVAS",
							"CVE_CLASE_GENERAL_INMUEBLES_ZONA",
							"CVE_NIVEL_SOCIO_ECONOMICO_ZONA",
							"CVE_CLASIFICACION_ZONA",
							"CVE_DENSIDAD_POBLACION",
							"CVE_REF_PROXIMIDAD_URBANA",
							"CVE_UBICACION_INMUEBLE_TERRENO",
							"DISTANCIA_UNIVERSIDAD",
							"DISTANCIA_CENTRO_DEPORTIVO",
							"DISTANCIA_CANCHAS_DEPORTIVAS",
							"DISTANCIA_MERCADOS",
							"DISTANCIA_PARQUES",
							"DISTANCIA_PLAZASPUBLICAS",
							"DISTANCIA_JARDINES",
							"DISTANCIA_SUPERMERCADOS",
							"DISTANCIA_IGLESIA",
							"NUMERO_ESTACIONAMIENTOS",
							"NUMERO_RECAMARAS",
							"SUPERFICIE_VENDIBLE",
							"FZO",
							"FFR",
							"w_avaluo2.IMPORTE_TOTAL_ENFOQUE_DE_COSTOS",
							"w_avaluo2.VALOR_COMPARATIVO_INMUEBLE_M2",
							"w_avaluo2.IMPORTE_VALOR_CONCLUIDO"
							]




	not_null_fields = [ 	
							"LONGITUD",
							"LATITUD",
							"NUMERO_RECAMARAS",
							"SUPERFICIE_VENDIBLE",
							"IMPORTE_TOTAL_ENFOQUE_DE_COSTOS",
							"VALOR_COMPARATIVO_INMUEBLE_M2",
							"IMPORTE_VALOR_CONCLUIDO"
							]

	select_fields_txt = [ 	
							"LONGITUD",
							"LATITUD",
							"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE",
							"CLAVE_MUNICIPIO_UBICACION_INMUEBLE",
							"CAT_TIPO_INMUEBLE",
							"CVE_NIVEL_INFRAESTR_URBANA",
							"CVE_NIVEL_EQUIPAMIENTO_URBANO",
							"CVE_CLASE_INMUEBLE",
							"CVE_USO_CONSTRUCCION",
							"FACTOR_RESULTANTE_PRIVATIVAS",
							"FACTOR_EDAD_PRIVATIVAS",
							"FACTOR_CONSERVACION_PRIVATIVAS",
							"CVE_CLASE_GENERAL_INMUEBLES_ZONA",
							"CVE_NIVEL_SOCIO_ECONOMICO_ZONA",
							"CVE_CLASIFICACION_ZONA",
							"CVE_DENSIDAD_POBLACION",
							"CVE_REF_PROXIMIDAD_URBANA",
							"CVE_UBICACION_INMUEBLE_TERRENO",
							"DISTANCIA_UNIVERSIDAD",
							"DISTANCIA_CENTRO_DEPORTIVO",
							"DISTANCIA_CANCHAS_DEPORTIVAS",
							"DISTANCIA_MERCADOS",
							"DISTANCIA_PARQUES",
							"DISTANCIA_PLAZASPUBLICAS",
							"DISTANCIA_JARDINES",
							"DISTANCIA_SUPERMERCADOS",
							"DISTANCIA_IGLESIA",
							"NUMERO_ESTACIONAMIENTOS",
							"NUMERO_RECAMARAS",
							"SUPERFICIE_VENDIBLE",
							"FZO",
							"FFR",
							"IMPORTE_TOTAL_ENFOQUE_DE_COSTOS",
							"VALOR_COMPARATIVO_INMUEBLE_M2",
							"IMPORTE_VALOR_CONCLUIDO"
							]




	def is_num(self, s):
		if s != "" and s != None:
			try: 
				int(s)
				return True
			except ValueError:
				try: 
					float(s)
					return True
				except ValueError:
					return False
		else:
			return False

	def get_avaluos_server(self, filters):
		'conectando a la base de datos...'
		filter_stm = ""
		for each_field in filters:
			element = "("
			for each_value in filters[each_field]:
				element += str(each_field) + "='"+str(each_value)+"' OR "
			element = element[:-3]
			element += ")"
			filter_stm += element + " AND "

		filter_stm = filter_stm[:-4]

		select_fields_stm = ", ".join(self.select_fields)
		print "filter stm: ", filter_stm
		print "select stm: ", select_fields_stm
		
		conn = pymssql.connect(server=self.server, user=self.user, password=self.password, database=self.database)  
		cursor = conn.cursor(as_dict=True)
		query_stm = "SELECT " + select_fields_stm + " FROM w_avaluo1 join w_avaluo2 on w_avaluo1.id2 = w_avaluo2.id2 WHERE " + filter_stm + " ;"

		print "Conexion iniciada con el servidor de datos"
		print "Ejecutando consulta..."
		print query_stm
		
		cursor.execute(query_stm)

		lista_avaluos = []
		c = 1
		for row in cursor:
			nuevo_avaluo = {}
			inconsistency_flag = True
			for each_field in row:
				if self.is_num(row[each_field]):
					if c == 1:
						print "campo: ", each_field, " es numerico"
					nuevo_avaluo[each_field] = float(row[each_field])

					if each_field == "IMPORTE_TOTAL_ENFOQUE_DE_COSTOS" and nuevo_avaluo[each_field] < 100000:
						inconsistency_flag = False
						print "appraisal will be discarted"
					elif each_field  == "VALOR_COMPARATIVO_INMUEBLE_M2" and nuevo_avaluo[each_field] < 1000:
						inconsistency_flag = False
						print "appraisal will be discarted"
					elif each_field  == "IMPORTE_VALOR_CONCLUIDO" and nuevo_avaluo[each_field] < 400000:
						inconsistency_flag = False
						print "appraisal will be discarted"

					elif each_field  == "LONGITUD" and nuevo_avaluo[each_field] > 0:
						nuevo_avaluo["LONGITUD"] = -1 * nuevo_avaluo["LONGITUD"]
					elif each_field  == "LATITUD" and nuevo_avaluo[each_field] < 0:
						nuevo_avaluo["LATITUD"] = -1 * nuevo_avaluo["LATITUD"]

					elif str(each_field).startswith("DISTANCIA"):
						if nuevo_avaluo[each_field] < 1:
							nuevo_avaluo[each_field] = 2000

				else:
					print "campo: ", each_field, " no es numerico"
					nuevo_avaluo[each_field] = 0.0
					if each_field in not_null_fields:
						inconsistency_flag = False
						print "appraisal will be discarted"
			if inconsistency_flag:
				lista_avaluos.append(nuevo_avaluo)
				print c,"-----> INMUEBLE  agregado con ", len(nuevo_avaluo), "  campos"
				c += 1
		
		return lista_avaluos


	def get_avaluos_csv(self, csv_file):
		'leyendo csv...'
		try:
			lista_avaluos = []
			raw_data = csv.DictReader(open(csv_file))
			#print "Data loaded!", raw_data
			for each_row in raw_data:
				lista_avaluos.append(each_row)
			return lista_avaluos
		except ValueError:
			print "Error: " + str(ValueError)	
			return []
		
