from django.shortcuts import render,redirect
from .models import Client,Facture,Produit,Stock,Prix,Avoir
from django.http import HttpResponse 
from .forms import FactureForm,produitFacture,prixFacture,qtAchete
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
    if request.method == 'POST':
        form_produit = produitFacture(request.POST)
        form_prix = prixFacture(request.POST)
        form_avoir = qtAchete(request.POST)
        if form_produit.is_valid() and form_prix.is_valid() and form_avoir.is_valid():
            msg = "produit ajoute avec succes, ajouter un autre."
            idP = Produit.objects.get(designation = form_produit.cleaned_data['designation']).CodeP
            prixU = form_prix.cleaned_data['PrixUnite']
            prixV = form_prix.cleaned_data['PrixVente']
            if Prix.objects.filter(PrixUnite = prixU, PrixVente = prixV).exists():
              idPrix = Prix.objects.get(PrixUnite = prixU,PrixVente = prixV).id
            else : 
                form_prix.save()
                idPrix = Prix.objects.latest('id').id
            idF = Facture.objects.latest('numero').numero
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
    context = { 'form_produit' : form_produit,
                'form_prix' : form_prix,
                'form_avoir' : form_avoir,
                'msg' : msg,
    }

    return render(request,"produitFacture.html",context)
    

def updateStock(idP,idPrix,qta):
    if Stock.objects.filter(produit_id = idP,Prix_id = idPrix).exists():
        print("in")
        instance = Stock.objects.get(produit_id = idP,Prix_id = idPrix)
        instance.Qtp += qta
        instance.save()
    else :
        Stock.objects.create(Qtp = qta,produit_id = idP,Prix_id = idPrix)