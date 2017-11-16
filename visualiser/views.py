from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def index(request):
    return HttpResponse('index')

def latest(request):
    return render(request, 'visualiser/latest.html', {})