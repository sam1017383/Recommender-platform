import sys
sys.path.insert(0, '/Library/Python/2.7/site-packages/pybrain-master')
import pymssql  
#conn = pymssql.connect(server='go4it.supportdesk.com.mx', user='userAvaluos', password='M3x1c087')  

conn = pymssql.connect(server='192.168.0.172', user='userAvaluos', password='M3x1c087')  




use Avaluos;
/*SELECT * FROM information_schema.tables WHERE TABLE_TYPE='BASE TABLE';*/
/*Select * From w_avaluo1 where CODIGOPOSTAL='14370';*/

Select * From INFORMATION_SCHEMA.COLUMNS Where TABLE_NAME = 'w_avaluo1';

query para separar todo el df tomó 7:30 min 



select codigo_postal_ubicacion_inmueble, count (*) as avaluos
from w_avaluo1
group by codigo_postal_ubicacion_inmueble
order by avaluos desc




Select 
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

					From w_avaluo1 inner join w_avaluo2 on w_avaluo1.id2 = w_avaluo2.id2
				Where codigo_postal_ubicacion_inmueble = '03100'







