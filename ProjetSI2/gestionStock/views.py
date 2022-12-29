from django.shortcuts import render
from .models import Client

# Create your views here.

def afficher_client(request):
    clients = Client.objects.all()
    return render(request,"Clients.html",{"clients":clients})

