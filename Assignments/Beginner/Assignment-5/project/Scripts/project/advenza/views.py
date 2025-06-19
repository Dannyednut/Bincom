from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import advenza_user

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def register(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render({'message': ''}, request))

def download(request):
    template = loader.get_template('download.html')
    return HttpResponse(template.render({}, request))

def record(request):
    name = request.POST['name']
    email = request.POST['email']
    gender = request.POST['gender']

    new_user = advenza_user(name=name, email=email, gender=gender)
    new_user.save()
    template = loader.get_template('register.html')
    message = 'Application received! We\'ll update you soon.'
    return HttpResponse(template.render({'message': message}, request))
# Create your views here.


