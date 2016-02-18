# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404 
from django.conf.urls.static import static
from django.http import Http404, HttpResponse
from django.template import Context, loader
from products.models import *

import recomendaciones_conocimiento
import datetime

# Create your views here.

#- Medatados del usuario
#  - productos_busqueda - Resultados de búsqueda
#  - productos_calificados - Mis productos calificados
#  - productos_similares - Productos similares a los que me han gustado
#  - productos_perfil - Recomendaciones a mi perfil
#  - productos_contenido - A usuarios similares les ha gustado
#  - productos_fc - Los productos mejor apreciados


def index(request):

    if request.user.is_authenticated():
        usuario = Users.objects.get(pk=request.user.id)
        nombre_usuario = usuario.Nombre +  " " + usuario.Apellido_p
    else:
        usuario = Users.objects.all()[3]
        nombre_usuario = "Usuario anónimo"



    productos_busqueda = Product.objects.order_by('?')[1:20]
    
    calificaciones = Calificaciones.objects.filter(users=usuario.id)

    consulta  = ""
    for each in calificaciones:
        consulta = consulta + "Product.objects.filter(pk=" + str(each.product.id) + ") | "
    consulta = consulta[:len(consulta)-2]
    productos_calificados = eval(consulta)

    productos_similares, metadatos_recomendacion3 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)

    
    productos_perfil, metadatos_recomendacion4 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)

    
    productos_contenido, metadatos_recomendacion4 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)

    
    productos_fc, metadatos_recomendacion4 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)

    template = loader.get_template('products/index.html')
    
    perfil_usuario = recomendaciones_conocimiento.perfil_usuario(usuario)

    context = {
        'nombre_usuario_saludo': nombre_usuario,
        'perfil': perfil_usuario,
        'productos_busqueda': productos_busqueda,
        'productos_calificados': productos_calificados,
        'productos_similares': productos_similares[:100],
        'productos_perfil': productos_perfil[:100],
        'productos_contenido': productos_similares[:100],
        'productos_fc': productos_similares[:100]
    }
    return HttpResponse(template.render(context, request))

def detail(request, product_id):

    #Buscar Lista de Productos recomendados para el usuario
    valorCalificacion = 0
    usuario = Users.objects.get(pk=request.user.id)
    product_list = Product.objects.all()[1:3]
    latest_productos_list, metadatos_recomendacion = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)
    
    #Busca el producto seleccionado
    Producto = get_object_or_404(Product, pk=product_id)

    #Busca objeto de Producto con calificacion para el usuario
    try:
        calificacionExistente = Calificaciones.objects.get(product=Producto, users=usuario)
    except Calificaciones.DoesNotExist:
        comentario = ""
        valorCalificacion = 0
        calificacionExistente = Calificaciones(product=Producto, users=usuario, calificacion_producto=valorCalificacion, comentario=comentario)

    if request.POST.get('comentario') is not None:
        comentario = request.POST.get('comentario')
#        comentario = unicode(comentario, "utf-8")
        calificacionExistente.calificacion_producto=valorCalificacion
        calificacionExistente.comentario=comentario
        calificacionExistente.save()
    else:
        if calificacionExistente.comentario is not None:
            comentario = calificacionExistente.comentario
        else:
            comentario = ""


    if request.POST.get('calificacion') is not None:
        valorCalificacion = request.POST.get('calificacion')
#        calificacionExistente = Calificacionx(productx=Producto, userx=usuario, calificacion_producto=valorCalificacion, comentario=comentario)
        calificacionExistente.calificacion_producto=valorCalificacion
        calificacionExistente.comentario=comentario
        calificacionExistente.save()
    else:
        if calificacionExistente.calificacion_producto is not None:
            valorCalificacion = calificacionExistente.calificacion_producto
        else:
            valorCalificacion = 0

    #Construcción del template y envío de Respuesta
    template = loader.get_template('products/detail.html')
    context = {
        'latest_productos_list': latest_productos_list[:150],
        'metadatos_usuario': metadatos_recomendacion,
        'Producto': Producto,
        'id_user': usuario.id,
        'calificacionExistente': calificacionExistente,
        'comentario': comentario,
        'valorCalificacion': valorCalificacion
    }

    return HttpResponse(template.render(context, request))