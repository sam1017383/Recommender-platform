# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404 
from django.conf.urls.static import static
from django.http import Http404, HttpResponse
from django.template import Context, loader
from products.models import *

import recomendaciones_conocimiento
import datetime

# Create your views here.
def index(request):
    product_list = Product.objects.all()[1:3]
    usuario = Users.objects.all()[0]
    latest_productos_list, metadatos_recomendacion = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)
    
    usuario2 = Users.objects.all()[0]
    latest_productos_list2, metadatos_recomendacion2 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario2)

    usuario3 = Users.objects.all()[0]
    latest_productos_list3, metadatos_recomendacion3 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario3)

    usuario4 = Users.objects.all()[0]
    latest_productos_list4, metadatos_recomendacion4 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario4)

    template = loader.get_template('products/index.html')
    context = {
        'latest_productos_list': latest_productos_list[:100],
        'metadatos_usuario': metadatos_recomendacion,
        'latest_productos_list2': latest_productos_list2[:100],
        'metadatos_usuario2': metadatos_recomendacion2,
        'latest_productos_list3': latest_productos_list3[:100],
        'metadatos_usuario3': metadatos_recomendacion3,
        'latest_productos_list4': latest_productos_list4[:100],
        'metadatos_usuario4': metadatos_recomendacion4
    }
    return HttpResponse(template.render(context, request))

def detail(request, product_id):

    #Buscar Lista de Productos recomendados para el usuario
    valorCalificacion = 0
    usuario_activo = request.user
    usuario = Users.objects.get(pk=usuario_activo.id)
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
        'id_user': usuario_activo.id,
        'calificacionExistente': calificacionExistente,
        'comentario': comentario,
        'valorCalificacion': valorCalificacion
    }

    return HttpResponse(template.render(context, request))