# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from itertools import cycle
import networkx as nx
import math
import random






# Cat.ClasesConstruccion  
# 0 NO APLICA
# 1 Mínima
# 2 Económica
# 3 Interés Social
# 4 Media
# 5 Semilujo
# 6 Residencial
# 7 Residencial Plus
# 7 Residencial Plus +
# 8 Única


# Cat.NivelInfraestructura  
# 1 No tiene alguno de los tres servicios básicos del nivel 2
# 2 Cuenta con agua potable, drenaje y luz en la zona
# 3 Cuenta con alumbrado público y vialidades terminadas (con banquetas) además de los servicios del nivel 2
# 4 Cuenta con gas natural y vigilancia privada además de los servicios del nivel 3.



# Cat.EstadoConservacion  
# 0 NO APLICA
# 1 RUINOSO
# 2 MALO
# 3 REGULAR
# 4 BUENO
# 5 MUY BUENO
# 6 NUEVO
# 7 RECIENTEMENTE REMODELADO



# Cat.NivelSocioeconomico 
# 0 No aplica
# 1 E Más bajo
# 2 D Bajo
# 3 D+ Medio Bajo
# 4 C Medio
# 5 C+ Medio Alto
# 6 A/B Alto


# Cat.NivelEquipamiento 
# 1 CUANDO EN LA ZONA EXISTAN DOS ELEMENTOS O MENOS DEL NIVEL 2.
# 2 CUANDO LA ZONA CUENTE CON  IGLESIA, MERCADO O COMERCIOS, ESCUELAS Y PARQUES Y JARDINES.
# 3 CUANDO LA ZONA TENGA LOS ELEMENTOS  DEL NIVEL 2 MÁS ACCESO O ESTACIÓN  DE TRANSPORTE PÚBLICO
# 4 CUANDO EN LA ZONA SE ENCUENTREN LOS ELEMENTOS DEL NIVEL 3 MÁS HOSPITALES Y BANCOS, MÁS OTROS EQUIPAMIENTOS



# Cat.DensidadHabitacional  
# 0 No aplica
# 1 Muy baja, 10 hab/ha una vivienda por lote de 1,000 m² 
# 2 Baja, 50 hab/ha una vivienda por lote de 500 m² 
# 3 Baja, 100 a 200 hab/ha una vivienda por lote de 250 m² 
# 4 Media, 400 hab/ha una vivienda por lote de 125 m² 
# 5 Alta, 800 hab/ha 


# Cat.Regimen 
# 1 PRIVADA
# 2 CONDOMINAL
# 3 COPROPIEDAD
# 4 PÚBLICA

# Cat.TipoInmueble  
# 1 TERRENO
# 2 CASA HABITACIÓN
# 3 CASA EN CONDOMINIO
# 4 DEPARTAMENTO EN CONDOMINIO
# 5 OTRO










def list_formated_appraisal(appraisal_dict):
  fields = appraisal_dict.keys()
  formated_list = []
  used_fields = []
  for each_field in fields:
    if each_field.startswith("IM_VENTAS_VALOR_") and each_field not in used_fields:
      formated_list.append(each_field + ": " + str(appraisal_dict[each_field]) + "   type: " + str(type(appraisal_dict[each_field])))
      used_fields.append(each_field)

  for each_field in fields:
    if each_field.startswith("CVE_") and each_field not in used_fields:
      formated_list.append(each_field + ": " + str(appraisal_dict[each_field]) + "   type: " + str(type(appraisal_dict[each_field])))
      used_fields.append(each_field)

  for each_field in fields:
    if each_field.startswith("CAT_") and each_field not in used_fields:
      formated_list.append(each_field + ": " + str(appraisal_dict[each_field]) + "   type: " + str(type(appraisal_dict[each_field])))
      used_fields.append(each_field)

  for each_field in fields:
    if (each_field == "LATITUD" or each_field == "LONGITUD") and each_field not in used_fields:
      formated_list.append(each_field + ": " + str(appraisal_dict[each_field]) + "   type: " + str(type(appraisal_dict[each_field])))
      used_fields.append(each_field)

  for each_field in fields:
    if each_field.startswith("NUMERO_") and each_field not in used_fields:
      formated_list.append(each_field + ": " + str(appraisal_dict[each_field]) + "   type: " + str(type(appraisal_dict[each_field])))
      used_fields.append(each_field)

  for each_field in fields:
    if each_field.startswith("DISTANCIA_") and each_field not in used_fields:
      formated_list.append(each_field + ": " + str(appraisal_dict[each_field]) + "   type: " + str(type(appraisal_dict[each_field])))
      used_fields.append(each_field)

  for each_field in fields:
    if each_field not in used_fields:
      formated_list.append(each_field + ": " + str(appraisal_dict[each_field]) + "   type: " + str(type(appraisal_dict[each_field])))

  return formated_list
    

header_html_js = """
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>UVs go4it</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>

function initMap() {

  var myLatLng = {lat: 19.37620830, lng: -99.1616527};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 14,
    center: myLatLng
  });
		"""
		

end_script = """
}

    </script>
    <script async defer
        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCZh54ICKZAQiPQ_-_ECdaEtWx_pcecJrM&signed_in=true&callback=initMap"></script>
  </body>
</html>

		"""






def dot_map_from_gps(gps_dicts, file_name):

	gen_map = open(file_name + ".html", "w+")
	pins = ""
	for each_dot in gps_dicts:
		pins += "var marker = new google.maps.Marker({position: {lat: " + str(each_dot["LATITUD"]) + "  , lng: " + str(each_dot["LONGITUD"]) + " }, map: map, title: 'Pin X!'}); \n"		
	code = header_html_js+pins+end_script
	gen_map.write(code)
	gen_map.close()
	return code


def format_module(a, b):
	n = a%b
	if n<10:
		return "00"+str(n)
	if n<100:
		return "0"+str(n)
	else:
		return str(n)

	

def format_price(int_price):
	n = int_price
	price_formated = ""
	while n >= 1:
		price_formated = "," + format_module(n,1000) +  price_formated
		n = n//1000

	price_chars = list(price_formated)
	i = 0
	cut = 0

	while i <len(price_chars):
		if price_chars[i] == "," or price_chars[i] == "0":
			cut += 1
			i += 1 
		else:
			break
	return price_formated[cut:]

def dot_infomap_from_appraisals(app_dicts, file_name):

  gen_map = open(file_name + ".html", "w+")
  c = 0
  pins = ""
  for each_dot in app_dicts:
    pins += """
  	var contentString = '<div id="content">'+
      '<div id="inmueble">'+
      '</div>'+
      '<h1 id="firstHeading" class="firstHeading"> $ """ + format_price(int(float(each_dot["IM_VENTAS_VALOR_MERCADO_INMUEBLE"]))) +  """</h1>'+
      '<div id="bodyContent">'+
      '<h2> M2: $""" + format_price(int(float(each_dot["IM_VENTAS_VALOR_UNITARIO_APLICABLE_AVALUO_M2"]))) +  """ </h2>' +
      '<h2> SUPERFICIE PRIVATIVAS: """ + str(each_dot["SUPERFICIE_PRIVATIVAS"]) +  """ m2 </h2>' +
      '<h2> SUPERFICIE TERRENO: """ + str(each_dot["SUPERFICIE_TERRENO"]) +  """ m2 </h2>' +
      '<h2> CODIGO POSTAL: """ + str(each_dot["codigo_postal_ubicacion_inmueble"]) +  """ </h2>' +
      '<h3> NUMERO_RECAMARAS: """ + str(each_dot["NUMERO_RECAMARAS"]) +  """ </h2>' +
      '<h3> NUMERO_ESTACIONAMIENTOS: """ + str(each_dot["NUMERO_ESTACIONAMIENTOS"]) +  """ </h2>' +
      '<h3> NUMERO_BANIOS: """ + str(each_dot["NUMERO_BANIOS"]) +  """ </h2>' +
      '<h3> NUMERO_MEDIOS_BANOS: """ + str(each_dot["NUMERO_MEDIOS_BANOS"]) +  """ </h2>' +
      '<h3> ELEVADOR: """ + str(each_dot["ELEVADOR"]) +  """ </h2>' +
      '<h2> -----------: """ + """ </h2>' +
      '<h3> CVE_NIVEL_SOCIO_ECONOMICO_ZONA: \t """ + str(each_dot["CVE_NIVEL_SOCIO_ECONOMICO_ZONA"]) +  """ </h2>' +
      '<h3> CVE_DENSIDAD_HABITACIONAL: """ + str(each_dot["CVE_DENSIDAD_HABITACIONAL"]) +  """ </h2>' +
      '<h3> CVE_ESTADO_CONSERVACION: """ + str(each_dot["CVE_ESTADO_CONSERVACION"]) +  """ </h2>' +
      '<h3> CVE_NIVEL_INFRAESTR_URBANA: """ + str(each_dot["CVE_NIVEL_INFRAESTR_URBANA"]) +  """ </h2>' +
      '<h3> INDICE_SATURACION_ZONA: """ + str(each_dot["INDICE_SATURACION_ZONA"]) +  """ </h2>' +
      '<h3> DISTANCIA_UNIVERSIDAD: """ + str(each_dot["DISTANCIA_UNIVERSIDAD"]) +  """ m </h2>' +
      '<h3> DISTANCIA_LOCALES_COMERCIALES: """ + str(each_dot["DISTANCIA_LOCALES_COMERCIALES"]) +  """ m </h2>' +
      '<h3> DISTANCIA_PARQUES: """ + str(each_dot["DISTANCIA_PARQUES"]) +  """ m </h2>' +
      '<h3> DISTANCIA_PLAZASPUBLICAS: """ + str(each_dot["DISTANCIA_PLAZASPUBLICAS"]) +  """ m </h2>' +
      '<h3> DISTANCIA_JARDINES: """ + str(each_dot["DISTANCIA_JARDINES"]) +  """ m </h2>' +
      '<h3> DISTANCIA_SUPERMERCADOS: """ + str(each_dot["DISTANCIA_JARDINES"]) +  """ m </h2>' +
      '<h3> DISTANCIA_IGLESIA: """ + str(each_dot["DISTANCIA_JARDINES"]) +  """ m </h2>' +
      '<h3> DISTANCIA_SERVICIOS_SALUD_PRIMER_NIVEL_: """ + str(each_dot["DISTANCIA_JARDINES"]) +  """ m </h2>' +

      
      '</div>'+
      '</div>';

  	var infowindow"""+ str(c) +  """ = new google.maps.InfoWindow({
    content: contentString
  });


	var marker"""+ str(c) +  """ = new google.maps.Marker({position: {lat: """ + str(each_dot["LATITUD"]) + "  , lng: " + str(each_dot["LONGITUD"]) + """ }, map: map, title: 'Pin X!'}); \n

	marker"""+ str(c) +  """.addListener('click', function() {
    infowindow"""+ str(c) +  """.open(map, marker"""+ str(c) +  """);
  });

"""
    c += 1

  code = header_html_js+pins+end_script
  gen_map.write(code)
  gen_map.close()

  return code






