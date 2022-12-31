import mimetypes
from django.shortcuts import render
from .models import *
from .forms import *
from . import functions
from datetime import datetime
from django.http.response import HttpResponse
import os

# Create your views here.

def afficher_client(request):
    clients = Client.objects.all()
    return render(request,"Clients.html",{"clients":clients})


def afficher_fournisseur(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request,"Fournisseurs.html",{"fournisseurs":fournisseurs})

def créer_bon_commande(request):
    file = ''
    if request.method == 'POST':
        form = BCForm(request.POST)
        if form.is_valid():
            now = datetime.now().strftime('%d%m%y %H%M%S')
            file = functions.pdf_gen(functions.cleaning_post_info(request.POST),f'./gestionStock/files/BonCommande {now}.pdf')
            return render(request,"BonDeCommande.html",{"form":form,"file":file})
    else:
        form = BCForm()
        return render(request,"BonDeCommande.html",{"form":form,"file":file})

def download_file(request, filename):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/files"

    if not filename :
        filename = "doc"

    filepath = BASE_DIR + "/" + filename

    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filepath.split("/")[-1]
        # Return the response value
    return response