from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Product
from .models import User


def index(request):
    
    product_list = Product.objects.all()
    template = loader.get_template('recomendador/index.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))
# Create your views here.
