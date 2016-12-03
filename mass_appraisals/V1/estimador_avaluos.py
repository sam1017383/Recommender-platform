# -*- coding: utf-8 -*-

from clustering import clustering_engine, cluster 
from data_manager import data_manager 



class regresor():

	data_man = data_manager()
	cluster_eng = clustering_engine()


	filtros_cubo_cdmx_departamentos_media = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3', '4'], "GRADO_TERMINACION_OBRA": ['100', '100.0', '100.00']}
	filtros_cubo_cdmx_departamentos_plus = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['5'], "CVE_CLASIFICACION_ZONA": [ '3', '2'], "GRADO_TERMINACION_OBRA": ['100', '100.0', '100.00']}
	filtros_cubo_cdmx_departamentos_alta = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['09'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['6'], "CVE_CLASIFICACION_ZONA": [ '3', '4'], "GRADO_TERMINACION_OBRA": ['100', '100.0', '100.00']}

	filtros_cubo_jalisco_departamentos_media = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['14'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3', '4'], "GRADO_TERMINACION_OBRA": ['100', '100.0', '100.00']}
	filtros_cubo_jalisco_departamentos_plus = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['14'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['5'], "CVE_CLASIFICACION_ZONA": [ '3', '2'], "GRADO_TERMINACION_OBRA": ['100', '100.0', '100.00']}
	filtros_cubo_jalisco_departamentos_alta = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['14'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['6'], "CVE_CLASIFICACION_ZONA": [ '3', '2'], "GRADO_TERMINACION_OBRA": ['100', '100.0', '100.00']}

	filtros_cubo_nuevo_leon_departamentos_media = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['19'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['4'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['4'], "CVE_CLASIFICACION_ZONA": [ '3', '4'], "GRADO_TERMINACION_OBRA": ['100', '100.0', '100.00']}
	filtros_cubo_nuevo_leon_departamentos_plus = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['19'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['5'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['5'], "CVE_CLASIFICACION_ZONA": [ '3', '2'], "GRADO_TERMINACION_OBRA": ['100', '100.0', '100.00']}
	filtros_cubo_nuevo_leon_departamentos_alta = {"CLAVE_ENTIDAD_FEDERATIVA_UBICACION_INMUEBLE": ['19'],"CAT_TIPO_INMUEBLE":['4'], "CVE_USO_CONSTRUCCION":['1'], "CVE_CLASE_INMUEBLE":['6', '7'], "CVE_NIVEL_SOCIO_ECONOMICO_ZONA":['6'], "CVE_CLASIFICACION_ZONA": [ '2', '1'], "GRADO_TERMINACION_OBRA": ['100', '100.0', '100.00']}









	def clusterizar(self, filtros_cubo, prefijo):
		avaluos = self.data_man.get_avaluos_server(filtros_cubo)
		num_clusters = len(avaluos)//40

		print "calculando ", num_clusters, " clusters"

		clusters = self.cluster_eng.get_clusters(prefijo, avaluos, num_clusters, 200, False)
		
		for each_cluster in clusters:
			each_cluster.update_statistics
			



	def analizar_clusters(self, prefijo, num_clusters):
		# filtros_cubo_cdmx_departamentos_plus43

		for c in range(num_clusters):
			file_name = prefijo + str(c)+".csv"

			avaluos = self.data_man.get_avaluos_csv(file_name)

			print "cluster: ", c, "  contiene: ", len(avaluos), " avaluos"











	def __init__(self):
		print "Iniciando experimento..."

		#self.clusterizar(self.filtros_cubo_cdmx_departamentos_plus, "filtros_cubo_cdmx_departamentos_plus")
		self.clusterizar(self.filtros_cubo_cdmx_departamentos_media, "filtros_cubo_cdmx_departamentos_media")
		self.clusterizar(self.filtros_cubo_cdmx_departamentos_plus, "filtros_cubo_cdmx_departamentos_plus")
		self.clusterizar(self.filtros_cubo_cdmx_departamentos_alta, "filtros_cubo_cdmx_departamentos_alta")
		self.clusterizar(self.filtros_cubo_jalisco_departamentos_media, "filtros_cubo_jalisco_departamentos_media")
		self.clusterizar(self.filtros_cubo_jalisco_departamentos_plus, "filtros_cubo_jalisco_departamentos_plus")
		self.clusterizar(self.filtros_cubo_jalisco_departamentos_alta, "filtros_cubo_jalisco_departamentos_alta")
		self.clusterizar(self.filtros_cubo_nuevo_leon_departamentos_media, "filtros_cubo_nuevo_leon_departamentos_media")
		self.clusterizar(self.filtros_cubo_nuevo_leon_departamentos_plus, "filtros_cubo_nuevo_leon_departamentos_plus")
		self.clusterizar(self.filtros_cubo_nuevo_leon_departamentos_alta, "filtros_cubo_nuevo_leon_departamentos_alta")
		
		#self.analizar_clusters("filtros_cubo_cdmx_departamentos_plus", 126)



r = regresor()