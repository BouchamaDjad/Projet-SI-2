import mimetypes
from django.shortcuts import render,redirect
from .models import Client,Facture,Produit,Stock,Prix,Avoir,Fournisseur
from .forms import FactureForm,produitFacture,prixFacture,qtAchete,BCForm,BC_ProduitForm,OptionFacture
from . import functions
from datetime import datetime
from django.http.response import HttpResponse
from django.http import HttpResponse 

import os
# Create your views here.

def afficher_client(request):
    clients = Client.objects.all()
    return render(request,"Clients.html",{"clients":clients})

def saisie_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("produitsfacture")
    form = FactureForm()
    return render(request,"saisie_facture.html",{'form':form})

def produits_facture(request):
    idF = Facture.objects.latest('numero').numero
    facture = Facture.objects.get(numero = idF)
    for p in facture.avoir_set.all():
        print(p.produit)
        print(p.prix)
        print(p.qta)
    if request.method == 'POST':
        form_produit = produitFacture(request.POST)
        form_prix = prixFacture(request.POST)
        form_avoir = qtAchete(request.POST)
        if form_prix.is_valid() and form_avoir.is_valid() and form_produit.is_valid():
            msg = "produit ajoute avec succes, ajouter un autre."
            idP = Produit.objects.get(designation = form_produit.cleaned_data['designation']).CodeP
            prixU = form_prix.cleaned_data['PrixUnite']
            prixV = form_prix.cleaned_data['PrixVente']
            if Prix.objects.filter(PrixUnite = prixU, PrixVente = prixV).exists():
              idPrix = Prix.objects.get(PrixUnite = prixU,PrixVente = prixV).id
            else : 
                form_prix.save()
                idPrix = Prix.objects.latest('id').id
            qta = form_avoir.cleaned_data['qta']
            Avoir.objects.create(qta = qta,facture_id = idF,produit_id = idP,prix_id = idPrix)
            updateStock(idP,idPrix,qta)
        else :
           msg = "erreur reessayer"
    else :
        msg = "Ajouter un produit a la facture"
    form_produit = produitFacture()
    form_prix = prixFacture()
    form_avoir = qtAchete()
    context = { 'id': idF,
                'form_prix' : form_prix,
                'form_avoir' : form_avoir,
                'msg' : msg,
                'choices' :form_produit.fields['designation'].choices,
    }

    return render(request,"produitFacture.html",context)
    

def updateStock(idP,idPrix,qta):
    if Stock.objects.filter(produit_id = idP,Prix_id = idPrix).exists():
        instance = Stock.objects.get(produit_id = idP,Prix_id = idPrix)
        instance.Qtp += qta
        instance.save()
    else :
        Stock.objects.create(Qtp = qta,produit_id = idP,Prix_id = idPrix)

def afficher_fournisseur(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request,"Fournisseurs.html",{"fournisseurs":fournisseurs})

def créer_bon_commande(request):
    file = ''
    if request.method == 'POST':
        form = BCForm(request.POST)

        produit_form_list = []
        error = False

        #3 = n° tuple produits
        #4 = n° tuple quantité
        req = list(request.POST.lists())[3:] #une liste des 2-tuple (key:list(val))

        for i in range(len(req[0][1])):
            bc_form = BC_ProduitForm({'produits':int(req[0][1][i]),
                                      'quantité':int(req[1][1][i])})
            if bc_form.is_valid():
                produit_form_list.append(bc_form)
            else:
                error = True
                break

        if form.is_valid() and not error:
            now = datetime.now().strftime('%d%m%y %H%M%S')
            file = functions.pdf_gen(functions.cleaning_post_info(request.POST),f'./gestionStock/files/BonCommande {now}.pdf')
            return render(request,"BonDeCommande.html",{"form":form,
                                                        "file":file,
                                                        "listproduitform":produit_form_list})
    
    form = BCForm()
    produit_form_list = [BC_ProduitForm()]
    return render(request,"BonDeCommande.html",{"form":form,
                                                "file":file,
                                                "listproduitform":produit_form_list})

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

def afficher_facture(request, pk):
    facture = Facture.objects.get(numero = pk)
    HT = 0
    if request.method == 'POST' :
        form = OptionFacture(request.POST)
        if form.is_valid():
           r = form.cleaned_data["remise"]
           if not form.cleaned_data["payer"]:
              for p in facture.avoir_set.all():
                  HT += p.prix.PrixUnite * p.qta
                  TTC = HT + HT * 0.19 
              if r != 0:
                  TTC = HT - HT * r/100
              facture.fournisseur.solde += TTC
              facture.sommeRestante = TTC
              facture.fournisseur.save()
           facture.remise = r
           facture.save()
           return redirect('saisiefacture')
    
    for p in facture.avoir_set.all():
        HT += p.prix.PrixUnite * p.qta
    TTC = HT + HT * 0.19
    form = OptionFacture()
    return render(request,"Facture.html",{"facture": facture,"TTC":TTC,"form":form})
