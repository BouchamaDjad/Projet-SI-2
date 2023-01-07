import mimetypes
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from . import functions
from datetime import datetime
from django.http.response import HttpResponse
from django.http import HttpResponse 
from django.db.models import F
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


def reglement_facture(request):
    msg = "entrez"
    formF = SelectionFournisseur()
    formR = reglementFacture()
    context = {
        "formF":formF,
        "formR" : formR,
        "choices" : formF.fields['Fournisseur'].choices,
        "msg" : msg,
    }
    return render(request,'reglementfacture.html',context)

def regler_factures(request):
    if request.method == 'POST':
        formF = SelectionFournisseur(request.POST)
        formR = reglementFacture(request.POST)
        if formF.is_valid() and formR.is_valid():
            idF = formF.cleaned_data["Fournisseur"]
            fournisseur = Fournisseur.objects.get(id = idF)
            factures = fournisseur.facture_set.filter(sommeRestante__gt = 0).order_by("numero")
            formR.save()
            return render(request,"reglerFactures.html",{"factures":factures,"idF":idF})
        else:
            return redirect("reglementfacture")

def sauv_reg(request, pk):
    if request.method == "POST":
        fournisseur = Fournisseur.objects.get(id = pk)
        factures = fournisseur.facture_set.filter(sommeRestante__gt = 0).order_by("numero")
        valeurs = request.POST.getlist('valeur[]')
        instance = ReglementFacture.objects.latest('id')
        filled = False
        date = instance.date
        ids = []
        for f in factures:
            ids.append(f.numero)
        
        for (v,n) in zip(valeurs,ids):
            if(float(v) != 0):
                if(not filled):
                    print(v,n)
                    instance.facture_id = n
                    instance.sommeAjoute = v
                    instance.save()
                    filled = True
                else :
                    print(v,n)
                    ReglementFacture.objects.create(date = date,sommeAjoute = v, facture_id = n)
                Facture.objects.filter(numero = n).update(sommeRestante = F('sommeRestante') - v)
        
        if(not filled):
            instance.delete()
        
        return redirect("clients")
  
def afficher_stock(request):
    stock = Stock.objects.exclude(id__in=SortieStock.objects.all().values('stock_id'))           

    if request.GET:
        form = FiltreForm(request.GET)
        if form.is_valid():
            if form.cleaned_data["type"]:
                stock = stock.filter(produit__typeP__designation=form.cleaned_data["type"])
            if form.cleaned_data["date"]:
                stock = stock.filter(Date=form.cleaned_data["date"])
            if form.cleaned_data['quantité']:
                stock = stock.filter(Qtp__lte=form.cleaned_data['quantité'])
            if form.cleaned_data['designation_produit']:
                stock = stock.filter(produit__designation__contains=form.cleaned_data['designation_produit'])
    else:
        form = FiltreForm()

    produits : list[dict] = [] 
    Total_achat = 0
    Total_vente = 0
    for s in stock:
        instance_prix = Prix.objects.get(id = s.Prix_id)
        Total_achat += s.Qtp * instance_prix.PrixUnite
        Total_vente += s.Qtp * instance_prix.PrixVente

        trv = False
        for p in produits:
            if p["produit"].CodeP == s.produit_id and p["prix"].id == s.Prix_id:
                p["qt"] += s.Qtp
                trv = True
                break

        if not trv:
            produits.append({"produit":Produit.objects.get(CodeP = s.produit_id),
                             "prix":Prix.objects.get(id = s.Prix_id),
                             "qt":s.Qtp,
                             "s":s.id})

    benefice = Total_vente - Total_achat

    return render(request,"Stock.html",{"form":form,
                                        "produits":produits,
                                        "Total_achat":Total_achat,
                                        "Total_vente":Total_vente,
                                        "benefice":benefice })

def ajuster_stock(request,pk,ppk):
    if request.method == 'POST':
        form = StockForm(request.POST)
        
        if form.is_valid():
            
            if not Prix.objects.filter(PrixUnite=form.cleaned_data['prixHT'],PrixVente=form.cleaned_data['prixVente']).exists():
                Prix.objects.create(PrixUnite=form.cleaned_data['prixHT'],PrixVente=form.cleaned_data['prixVente'])
                                      
            
            if Stock.objects.filter(produit_id = int(form.cleaned_data['codeP']),
                                    Prix__PrixUnite = form.cleaned_data['prixHT'],
                                    Prix__PrixVente=form.cleaned_data['prixVente']).exists():

                instance = Stock.objects.get(produit_id = int(form.cleaned_data['codeP']),
                                             Prix__PrixUnite = form.cleaned_data['prixHT'],
                                             Prix__PrixVente=form.cleaned_data['prixVente'])
                instance.Qtp = form.cleaned_data['Qtp'] # optimisation possible
                instance.save()
            else:
                prix_id = Prix.objects.get(PrixUnite = form.cleaned_data['prixHT'],PrixVente=form.cleaned_data['prixVente']).id
                instance = Stock.objects.create(produit_id = int(form.cleaned_data['codeP']),Prix_id=prix_id,Qtp=form.cleaned_data['Qtp'])

            return redirect('stock')

    stock=Stock.objects.filter(produit_id=pk,Prix_id=ppk)
    produit = {
        "produit":Produit.objects.get(CodeP=pk),
        "prix":Prix.objects.get(id=ppk),
        "qt":0
    }
    for s in stock:
        if s.Prix == produit["prix"]:
            produit["qt"] += s.Qtp

    form = StockForm({"codeP":pk,
                      "prixHT":produit["prix"].PrixUnite,
                      "prixVente":produit["prix"].PrixVente,
                      "Qtp":produit["qt"]})

    return render(request,"ajuster_stock.html",{'produit':produit,'form':form})

def entrer_en_stock(request):
    if request.method == 'POST':
        form = EntrerStockForm(request.POST)
        if form.is_valid():
            Produit.objects.create(CodeP=form.cleaned_data['CodeP'],
                                   designation=form.cleaned_data['Designation'],
                                   typeP = form.cleaned_data['Type'])
            EntreeStock.objects.create(date = form.cleaned_data['Date'],
                                       qt=form.cleaned_data['Quantité'],
                                       produit = Produit.objects.get(CodeP=form.cleaned_data['CodeP']))
            Stock.objects.create(date=form.cleaned_data['Date'],
                                 Qtp=form.cleaned_data['Quantité'],
                                 produit_id=form.cleaned_data['CodeP'])
            return redirect("entrystock")

    form = EntrerStockForm()
    entries = EntreeStock.objects.all()
    return render(request,"entry stock.html",{"form":form,"entries":entries})

def déstocker(request,pk):
    if request.method == 'POST':
        form = SortieStockForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            instance = Stock.objects.get(id=form.cleaned_data['stock'].id)
            instance.Qtp -= form.cleaned_data['qt']
            instance.save()
            return redirect('stock')
    
    form = SortieStockForm(initial={'stock':pk})
    return render(request,"DéStocker.html",{'form':form})

def sortie_stock(request):
    if request.method == 'POST':
        form = SortieStockForm(request.POST)
        if form.is_valid():
            form.save()
            instance = Stock.objects.get(id=form.cleaned_data['stock']) #
            instance.Qtp -= form.cleaned_data['qt'] #
            instance.save()
            return redirect('sortiestock')
    
    sorties = SortieStock.objects.all()
    form = SortieStockForm()
    return render(request,"Sortie Stock.html",{'sorties':sorties,'form':form})

def selection_client(request):
    clients = Client.objects.all()
    
    if request.GET:
        form = FiltreClient(request.GET)
        if form.is_valid():
            clients = Client.objects.filter(nom__contains = form.cleaned_data['nom'])

    else :
        form = FiltreClient()
    
    context = {
        "form": form,
        "clients": clients
    }

    return render(request,"selection_client.html",context)

def saisir_produit(request,pk):
    cl = Client.objects.get(id = pk)
    produits = Stock.objects.filter(Qtp__gt = 0)
    if request.GET:
        form = FiltreProduit(request.GET)
        if form.is_valid():
            produits = produits.filter(produit__designation__contains = form.cleaned_data['nom'])

    else :
        form = FiltreProduit()

    context = {
        "form" : form,
        "produits" : produits,
    }

    return render(request,"produitVente.html",context)
    