import mimetypes
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.utils.timezone import now
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from . import functions
from django.http.response import HttpResponse
from django.http import HttpResponse 
from django.db.models import F,Sum
import os
# Create your views here.

def afficher_client(request):
    clients = Client.objects.all()
    return render(request,"Clients.html",{"clients":clients})

def saisie_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            idFr = form.cleaned_data["fournisseur"].id
            return redirect("produitsfacture",pk = form.cleaned_data["numero"],idFr = idFr,date = str(date))
    form = FactureForm()
    return render(request,"saisie_facture.html",{'form':form})

def produits_facture(request,pk,idFr,date):
    idF = pk
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

            if not Facture.objects.filter(numero = idF).exists():
                Facture.objects.create(numero = idF,fournisseur_id = idFr,date = date)
            
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


def afficher_facture(request, pk):
    try :
        facture = Facture.objects.get(numero = pk)
    except Facture.DoesNotExist:
        return redirect("fournisseurs")
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
                  TTC = TTC - TTC * r/100
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


def reglement_facture(request):
    choices = []
    fournisseurs = Fournisseur.objects.all()
    for f in fournisseurs :
        choices.append((f.id,f'{f.nom} {f.prenom}'))
    formF = SelectionFournisseur(choices)
    formR = reglementFacture()
    context = {
        "formF":formF,
        "formR" : formR,
        "choices" : formF.fields['Fournisseur'].choices
    }
    return render(request,'reglementfacture.html',context)


def reglement_vente(request):
    choices = []
    clients = Client.objects.all()
    for f in clients :
        choices.append((f.id,f'{f.nom} {f.prenom}'))
    formC = SelectionClient(choices)
    formR = reglementVente()
    context = {
        "formC":formC,
        "formR" : formR,
        "choices" : formC.fields['Client'].choices,
    }
    return render(request,'reglementVente.html',context)

def regler_factures(request):
    if request.method == 'POST':
        formF = SelectionFournisseur(request.POST)
        formR = reglementFacture(request.POST)
        if formF.is_valid() and formR.is_valid():
            idF = formF.cleaned_data["Fournisseur"]
            fournisseur = Fournisseur.objects.get(id = idF)
            factures = fournisseur.facture_set.filter(sommeRestante__gt = 0).order_by("numero")
            date = formR.cleaned_data["date"]
            return render(request,"reglerFactures.html",{"factures":factures,"idF":idF,"date":date})
        else:
            return redirect("reglementfacture")

def regler_ventes(request):
    if request.method == 'POST':
        formC = SelectionClient(request.POST)
        formR = reglementVente(request.POST)
        if formC.is_valid() and formR.is_valid():
            idC = formC.cleaned_data["Client"]
            client = Client.objects.get(id = idC)
            ventes = client.vente_set.filter(restant__gt = 0).order_by("id")
            date = formR.cleaned_data["date"]
            return render(request,"reglerVentes.html",{"ventes":ventes,"idC":idC,"date":date})
        else:
            return redirect("reglementvente")

def sauv_reg(request,pk,date):
    if request.method == "POST":
        fournisseur = Fournisseur.objects.get(id = pk)
        factures = fournisseur.facture_set.filter(sommeRestante__gt = 0).order_by("numero")
        valeurs = request.POST.getlist('valeur[]')
        ids = []
        for f in factures:
            ids.append(f.numero)
        
        for (v,n) in zip(valeurs,ids):
            if(float(v) != 0): 
                ReglementFacture.objects.create(date = date,sommeAjoute = v, facture_id = n)
                Facture.objects.filter(numero = n).update(sommeRestante = F('sommeRestante') - v)
                fournisseur.solde -= float(v)
                fournisseur.save()

        return redirect("clients")

def sauv_regV(request,pk,date):
    if request.method == "POST":
        client = Client.objects.get(id = pk)
        ventes = client.vente_set.filter(restant__gt = 0).order_by("id")
        valeurs = request.POST.getlist('valeur[]')
        ids = []
        for v in ventes:
            ids.append(v.id)
        
        for (v,n) in zip(valeurs,ids):
            if(float(v) != 0):
                ReglementVente.objects.create(date = date,sommeAjoute = v, vente_id = n)
                Vente.objects.filter(id = n).update(restant = F('restant') - v)
                client.credit -= float(v)
                client.save()
        
        return redirect("reglementvente")
  
def afficher_stock(request):
    stock = Stock.objects.all()    

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

    Total_achat = 0
    Total_vente = 0
    for s in stock:
        try : 
            instance_prix = Prix.objects.get(id = s.Prix_id)
            if instance_prix:
                Total_achat += s.Qtp * instance_prix.PrixUnite
                Total_vente += s.Qtp * instance_prix.PrixVente
        except Prix.DoesNotExist:
            pass

    benefice = Total_vente - Total_achat

    return render(request,"Stock.html",{"form":form,
                                        "produits":stock,
                                        "Total_achat":Total_achat,
                                        "Total_vente":Total_vente,
                                        "benefice":benefice })

def ajuster_stock(request,s):
    stock=Stock.objects.get(id = s)
    if request.method == 'POST':
        form = StockForm(request.POST)
        
        if form.is_valid():
            if not Prix.objects.filter(PrixUnite=form.cleaned_data['prixHT'],PrixVente=form.cleaned_data['prixVente']).exists():
                Prix.objects.create(PrixUnite=form.cleaned_data['prixHT'],PrixVente=form.cleaned_data['prixVente'])
                                      
            stock.delete()
            if Stock.objects.filter(produit_id = int(form.cleaned_data['codeP']),
                                    Prix__PrixUnite = form.cleaned_data['prixHT'],
                                    Prix__PrixVente=form.cleaned_data['prixVente']).exists():

                instance = Stock.objects.get(produit_id = int(form.cleaned_data['codeP']),
                                             Prix__PrixUnite = form.cleaned_data['prixHT'],
                                             Prix__PrixVente=form.cleaned_data['prixVente'])
                instance.Qtp += form.cleaned_data['Qtp'] # optimisation possible
                instance.save()
            else:
                prix_id = Prix.objects.get(PrixUnite = form.cleaned_data['prixHT'],PrixVente=form.cleaned_data['prixVente']).id
                instance = Stock.objects.create(produit_id = int(form.cleaned_data['codeP']),Prix_id=prix_id,Qtp=form.cleaned_data['Qtp'])

            return redirect('stock')

    if stock.Prix:
        prixUnite = stock.Prix.PrixUnite
        prixVente:stock.Prix.PrixVente
    else:
        prixUnite = None
        prixVente=None
    form = StockForm({"codeP":stock.produit.CodeP,
                      "prixHT":prixUnite,
                      "prixVente":prixVente,
                      "Qtp":stock.Qtp})

    return render(request,"ajuster_stock.html",{'stock':stock,'form':form})

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
            Stock.objects.create(Date=form.cleaned_data['Date'],
                                 Qtp=form.cleaned_data['Quantité'],
                                 produit_id=form.cleaned_data['CodeP'])

    form = EntrerStockForm()
    entries = EntreeStock.objects.all()
    return render(request,"entry stock.html",{"form":form,"entries":entries})

def déstocker(request,pk):
    if request.method == 'POST':
        SortieStock.objects.create(motif=request.POST["motif"],qt = request.POST["qt"],stock_id = pk)
        instance = Stock.objects.get(id=pk)
        instance.Qtp -= int(request.POST['qt'])
        instance.save()
        return redirect('stock')
    
    return render(request,"DéStocker.html",{'max':Stock.objects.get(id = pk).Qtp})

def sortie_stock(request):
    sorties = SortieStock.objects.all()
    return render(request,"Sortie Stock.html",{'sorties':sorties})

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

def cree_clientV(request):
    if request.method == "POST":
        form = FormClient(request.POST)
        if form.is_valid:
            l = form.save()
            return redirect("saisirproduit",pk = l.id)
    
    form = FormClient()
    return render(request,"CreeClientVente.html",{"form":form})

def saisir_produit(request,pk):
    produits = Stock.objects.filter(Qtp__gt = 0,Prix__isnull = False)
    if request.GET:
        form = FiltreProduit(request.GET)
        if form.is_valid():
            produits = produits.filter(produit__designation__contains = form.cleaned_data['nom'])

    else :
        form = FiltreProduit()

    context = {
        "form" : form,
        "produits" : produits,
        "idC" : pk,
    }

    return render(request,"produitVente.html",context)


def saisir_produit2(request,v):
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
        "idV" : v,
    }

    return render(request,"produitVente2.html",context)
    

def quantite_produit(request,pk,s):
    p = Stock.objects.get(id = s)
    if request.method == 'POST':
        v = Vente.objects.create(client_id = pk).id
        qt = request.POST["qt"]
        Composer.objects.create(produit_id = p.produit.CodeP, prix_id = p.Prix.id, vente_id = v,QtV = qt)
        p.Qtp -= int(qt)
        p.save()
        return redirect("saisirproduit2", v=v) 
    return render(request,"quantiteVente.html",{"p":p})

def quantite_produit2(request,v,s):
    p = Stock.objects.get(id = s)
    if request.method == 'POST':
        qt = request.POST["qt"]
        Composer.objects.create(produit_id = p.produit.CodeP, prix_id = p.Prix.id, vente_id = v,QtV = qt)
        p.Qtp -= int(qt)
        p.save()
        return redirect("saisirproduit2", v=v) 
    return render(request,"quantiteVente2.html",{"p":p})

def payement_vente(request,v):
    vente = Vente.objects.get(id = v)
    total = 0
    for p in vente.composer_set.all():
        total += p.prix.PrixVente * p.QtV

    if request.method =="POST":
        if "status" not in request.POST:
            m = request.POST["montant"]
            cl = vente.client
            cl.credit += total - float(m)
            vente.restant = total - float(m)
            cl.save()
            vente.save()
        
        return redirect("selectionclient")


  
    return render(request,"FinaliserVente.html",{"vente":vente,"total": total})

def stats(request):
    first_day_of_this_month = now().replace(day=1)
    first_day_of_next_month = (
       first_day_of_this_month + timedelta(days=32)
    ).replace(day=1)
    first_day_of_twelve_months_ago = first_day_of_next_month - relativedelta(years=1)
    all_ventes = Composer.objects.all().values('produit','QtV','prix__PrixVente','prix__PrixUnite','vente__Date','vente__client')
    statsAnnee= all_ventes.values("vente__Date__year").annotate(montant = Sum(F('QtV') * F('prix__PrixVente'))).order_by("vente__Date__year")
    ventes12mois = Composer.objects.filter(vente__Date__gte = first_day_of_twelve_months_ago).values('QtV','prix__PrixVente','prix__PrixUnite','vente__Date')
    stats= ventes12mois.values("vente__Date__month").annotate(montant = Sum(F('QtV') * F('prix__PrixVente'))).order_by("vente__Date__month")
    a = statsAnnee.first()['vente__Date__year']
    label_annee = [a+i for i in range(statsAnnee.count()) ]
    
    BenificeAnnee= all_ventes.values("vente__Date__year").annotate(benifice = Sum(F('QtV') * (F('prix__PrixVente') - F('prix__PrixUnite')))).order_by("vente__Date__year")
    Benifice12mois= ventes12mois.values("vente__Date__month").annotate(benifice = Sum(F('QtV') * (F('prix__PrixVente') - F('prix__PrixUnite')))).order_by("vente__Date__month")
    
    total_achat_client = all_ventes.values("vente__client").annotate(total_achat = Sum(F('QtV') * F('prix__PrixVente')) - F('vente__client__credit')).order_by('-total_achat')

    classementCl = []
    l = list(total_achat_client)
    leng = len(l)
    i = 0
    while i<3 and i<leng:
        cl = Client.objects.get(id = l[i]['vente__client'])
        classementCl.append({
            'nom' : cl.nom,
            'prenom' : cl.prenom,
            'montant' : l[i]['total_achat']
        })
        i+=1
    
    q = all_ventes.values("produit").annotate(quantite = Sum('QtV')).order_by('-quantite')
    
    classementPr = []
    l = list(q)
    leng = len(l)
    i = 0
    while i<3 and i<leng:
        p = Produit.objects.get(CodeP = l[i]['produit'])
        classementPr.append({
            'designation' : p.designation,
            'quantite' : l[i]['quantite']
        })
        i+=1

    context = {
        'first_month' : first_day_of_next_month.month,
        'stats12mois':stats,
        'statsAnnee' : statsAnnee,
        'label_annee' : label_annee,
        'benificeAnnee' : BenificeAnnee,
        'benifice12mois' :Benifice12mois,
        'classementCl' : classementCl,
        'classementPr' : classementPr,
    }

    return render(request,"StatsVente.html",context)

def statsAchat(request):

    first_day_of_this_month = now().replace(day=1)
    first_day_of_next_month = (
       first_day_of_this_month + timedelta(days=32)
    ).replace(day=1)
    first_day_of_twelve_months_ago = first_day_of_next_month - relativedelta(years=1)

    all_achats = Avoir.objects.all().values('produit','qta','prix__PrixUnite','facture__date','facture__fournisseur')

    statsAnnee = all_achats.values("facture__date__year").annotate(montant = Sum(F('qta') * F('prix__PrixUnite'))).order_by("facture__date__year")
    
    achats12mois = Avoir.objects.filter(facture__date__gte = first_day_of_twelve_months_ago).values('qta','prix__PrixUnite','facture__date')

    stats = achats12mois.values("facture__date__month").annotate(montant = Sum(F('qta') * F('prix__PrixUnite'))).order_by("facture__date__month")
    
    a = statsAnnee.first()['facture__date__year']
    label_annee = [a+i for i in range(statsAnnee.count()) ]
                                                                                                                                    #- F('facture__fournisseur__solde')
    total_fournie_fournisseur = all_achats.values("facture__fournisseur").annotate(total_fournie = Sum(F('qta') * F('prix__PrixUnite'))).order_by('-total_fournie')

    classementF = []
    l = list(total_fournie_fournisseur)
    length = len(l)
    i = 0
    while i<3 and i<length:
        f = Fournisseur.objects.get(id = l[i]['facture__fournisseur'])
        classementF.append({
            'nom' : f.nom,
            'prenom' : f.prenom,
            'total' : l[i]['total_fournie']
        })
        i+=1
   

    plus_achetes = all_achats.values("produit").annotate(quantite = Sum('qta')).order_by('-quantite')
    classementPr = []
    l = list(plus_achetes)
    length = len(l)
    i = 0
    while i<3 and i<length:
        p = Produit.objects.get(CodeP = l[i]['produit'])
        classementPr.append({
            'CodeP':p.CodeP,
            'designation' : p.designation,
            'quantite' : l[i]['quantite']
        })
        i+=1



    context = {
        'first_month' : first_day_of_next_month.month,
        'stats12mois':stats,
        'statsAnnee' : statsAnnee,
        'label_annee' : label_annee,
        'classementF' : classementF,
        'classementPr' : classementPr,
    }

    return render(request,"StatsAchat.html",context)

def supprimer_client(request,pk):
    instance = Client.objects.get(id = pk)
    instance.delete()
    return redirect("clients")
    
def supprimer_fournisseur(request,pk):
    instance = Fournisseur.objects.get(id = pk)
    instance.delete()
    return redirect("fournisseurs")

def ajouter_fournisseur(request):
    if request.method == "POST":
        form = FormFournisseur(request.POST)
        if form.is_valid:
            form.save()
            return redirect("fournisseurs")
    
    form = FormClient()
    return render(request,"CreeFournisseur.html",{"form":form})

def edit_client(request,pk):
    client = Client.objects.get(id = pk)
    if request.method == 'POST':
        form = FormClient(request.POST,instance=client)
        if form.is_valid:
            form.save()
        return redirect('clients')
           
    

    form = FormClient(initial={
    'nom': client.nom, 
    'prenom':client.prenom,
    'phone':client.phone,
    'adresse':client.adresse
    })

    return render(request,"modifierClient.html",{"form":form})

def edit_fournisseur(request,pk):
    fournisseur = Fournisseur.objects.get(id = pk)
    if request.method == 'POST':
        form = FormFournisseur(request.POST,instance=fournisseur)
        if form.is_valid:
            form.save()
        return redirect('fournisseurs')
           
    form = FormFournisseur(initial={
    'nom': fournisseur.nom, 
    'prenom':fournisseur.prenom,
    'phone':fournisseur.phone,
    'adresse':fournisseur.adresse
    })

    return render(request,"modifierFournisseur.html",{"form":form})

def creation_client(request):
    if request.method == 'POST':
        form = FormClient(request.POST)
        if form.is_valid:
            form.save()
        return redirect('clients')
    form = FormClient()
    return render(request,"CreeClient.html",{"form":form})

def ajout_produit(request):
    if request.method == 'POST':
        form = FormProduit(request.POST)
        if form.is_valid:
            form.save()
        return redirect('stock')
    form = FormProduit()
    return render(request,"ajoutProduit.html",{"form":form})

def ajout_type(request):
    if request.method == 'POST':
        form = FormType(request.POST)
        if form.is_valid:
            print("n")
            form.save()
        return redirect('stock')
    form = FormType()
    return render(request,"ajoutType.html",{"form":form})

def afficher_type(request):
    produit_types = TypeProduit.objects.all()
    return render(request,"types produit.html",{"types":produit_types})

def supprimer_type(request,pk):
    instance = TypeProduit.objects.get(id = pk)
    instance.delete()
    return redirect('types produit') 

def edit_types(request,pk):
    if request.method == 'POST':
        form = FormType(request.POST)
        if form.is_valid():
            t = TypeProduit.objects.get(id = pk)
            t.designation = form.cleaned_data['designation']
            t.save()
        return redirect('types produit')
    
    form = FormType()
    return render(request,"editType.html",{"form":form})
