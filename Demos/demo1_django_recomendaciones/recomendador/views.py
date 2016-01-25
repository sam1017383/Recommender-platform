from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


from .models import Product
from .models import User

import recomendaciones_conocimiento



def index(request):
    product_list = Product.objects.all()[1:3]
    usuario = User.objects.all()[0]
    product_list_2 = recomendaciones_conocimiento.recomendacion_por_reglas(usuario)
    template = loader.get_template('recomendador/index.html')
    context = {
        'product_list': product_list_2,
    }
    return HttpResponse(template.render(context, request))
# Create your views here.
