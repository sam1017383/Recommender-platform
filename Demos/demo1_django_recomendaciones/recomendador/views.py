from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hola. Este es un recomendador automatico de productos.")
# Create your views here.
