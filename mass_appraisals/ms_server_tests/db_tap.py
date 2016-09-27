import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages/pybrain-master')
sys.path.insert(0, '/usr/local/lib/python2.7/site-packages')
import pymssql  
#conn = pymssql.connect(server='go4it.supportdesk.com.mx', user='userAvaluos', password='M3x1c087')  

# ejemplos como una lista de diccionarios
train_data = []

def is_num(s):
	if s != "":
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


conn = pymssql.connect(server='192.168.0.172', user='userAvaluos', password='M3x1c087', database='ExtracAvaluo')  

cursor = conn.cursor(as_dict=True)

cursor.execute("""Select top 10
						SUPERFICIE_TERRENO, 
						SUPERFICIE_PRIVATIVAS, 
						NUMERO_RECAMARAS,
						NUMERO_RECAMARAS,
						NUMERO_BANIOS,
						NUMERO_MEDIOS_BANOS,
						NUMERO_ESTACIONAMIENTOS,
						CVE_CLASE_INMUEBLE,
						CVE_ESTADO_CONSERVACION,
						ELEVADOR,
						INDICE_SATURACION_ZONA,
						CVE_DENSIDAD_HABITACIONAL,
						DENSIDAD_HABITACIONAL_VIVIENDAS,
						CVE_NIVEL_SOCIO_ECONOMICO_ZONA,
						NIVEL_INFRAESTRUCTURA,
						CVE_NIVEL_INFRAESTR_URBANA,
						CVE_NIVEL_EQUIPAMIENTO_URBANO,
						DISTANCIA_IGLESIA,
						DISTANCIA_BANCOS,
						DISTANCIA_CANCHAS_DEPORTIVAS,
						DISTANCIA_CENTRO_DEPORTIVO,
						DISTANCIA_PLAZASPUBLICAS,
						DISTANCIA_PARQUES,
						DISTANCIA_JARDINES,
						DISTANCIA_MERCADOS,
						DISTANCIA_SUPERMERCADOS,
						DISTANCIA_LOCALES_COMERCIALES,
						DISTANCIA_SERVICIOS_SALUD_PRIMER_NIVEL_,
						DISTANCIA_SERVICIOS_SALUD_SEGUNDO_NIVEL_,
						DISTANCIA_SERVICIOS_SALUD_TERCER_NIVEL_,
						DISTANCIA_ESCUELAS_PRIMARIAS,
						DISTANCIA_ESCUELAS_SECUNDARIAS,
						DISTANCIA_ESCUELAS_PREPARATORIA,
						DISTANCIA_UNIVERSIDAD,
						LONGITUD,
						LATITUD,
						codigo_postal_ubicacion_inmueble,
						CAT_REGIMEN_PROPIEDAD,
						CAT_TIPO_INMUEBLE,
						w_avaluo1.id2,
						w_avaluo2.IM_VENTAS_VALOR_UNITARIO_APLICABLE_AVALUO_M2,
						w_avaluo2.IM_VENTAS_VALOR_MERCADO_INMUEBLE

					From w_avaluo1 join w_avaluo2 on w_avaluo1.id2 = w_avaluo2.id2
				Where codigo_postal_ubicacion_inmueble = '45653'
				;
				""")

for row in cursor:
	new_train = {}
	for each_field in row:
		if is_num(row[each_field]):
			new_train[each_field] = row[each_field]
	print "-----> INMUEBLE  agregado con ", len(new_train), "  campos"
	train_data.append(new_train)


for each_train in train_data:
	print " INMUEBLE: ", each_train
	

	#for each_field in :
	#	print "      CAMPO: ", each_field, "   VALOR: ", each_train[each_field]
		



conn.close()