from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('Home Page')


def products(request):
    return HttpResponse('product lelo')


def coustomer(request):
    return HttpResponse('Jago grahak jaago .....jaag na bhsdk')       