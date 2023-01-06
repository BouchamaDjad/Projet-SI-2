from datetime import datetime
from django import forms
from .models import *

class ProduitField(forms.ModelChoiceField):
    class Meta:
        model = Produit
        field = ('CodeP','designation')

class FournisseurChoiceField(forms.ModelChoiceField):
    class Meta:
        model = Fournisseur
        field = ('nom','prenom')

class BC_ProduitForm(forms.Form):
    produits = ProduitField(Produit.objects.all())
    quantité = forms.IntegerField()

class BCForm(forms.Form):
    date = forms.DateTimeField(initial = datetime.now)
    fournisseur = FournisseurChoiceField(Fournisseur.objects.all())


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ('numero','date','fournisseur')
        widgets = {
            'date':forms.DateInput( attrs= {'type':'date'})
            
        }

class produitFacture(forms.Form):
    choices = []
    products = Produit.objects.all()
    for p in products :
        choices.append((p.designation,p.designation))
    designation = forms.ChoiceField(choices = tuple(choices))

class prixFacture(forms.ModelForm):
    class Meta : 
        model = Prix
        fields = '__all__'


class qtAchete(forms.ModelForm):
    class Meta :
        model = Avoir
        fields = ['qta']
        labels = {
            'qta':'Quantite',
        }

class OptionFacture(forms.Form):
    payer = forms.BooleanField(label='payer',required=False)
    remise = forms.FloatField(label = 'Remise (%)',initial=0)

class reglementFacture(forms.ModelForm):
    class Meta:
        model = ReglementFacture
        fields = ['date']
        widgets = {
            'date':forms.DateInput( attrs= {'type':'date'})
        }
    
class SelectionFournisseur(forms.Form):
    choices = []
    fournisseurs = Fournisseur.objects.all()
    for f in fournisseurs :
        choices.append((f.id,f'{f.nom} {f.prenom}'))
    Fournisseur = forms.ChoiceField(choices = tuple(choices))

class TypeProduitChoiceField(forms.ModelChoiceField):
    class Meta:
        model=TypeProduit
        field=['designation'] 
    
class FiltreForm(forms.Form):
    date = forms.DateField(required=False)
    type = TypeProduitChoiceField(TypeProduit.objects.all(),required=False)
    quantité = forms.IntegerField(label_suffix='<=',required=False)
    designation_produit = forms.CharField(required=False)

class StockForm(forms.Form):
    choice = [(p.CodeP,p.designation) for p in Produit.objects.all()]

    codeP = forms.ChoiceField(choices=choice,label="CodeP")
    prixHT = forms.FloatField(label="PrixHT")
    prixVente =  forms.FloatField(label="PrixVente")
    Qtp = forms.IntegerField(label="Quantité")

class EntrerStockForm(forms.Form):
    CodeP = forms.IntegerField(initial=Produit.objects.latest('CodeP').CodeP+1)
    Designation  = forms.CharField()
    Type = TypeProduitChoiceField(TypeProduit.objects.all())
    Date = forms.DateField(initial=datetime.today())
    Quantité = forms.IntegerField()

class FiltreClient(forms.Form):
   nom = forms.CharField(required=True)


class FiltreProduit(forms.Form):
   nom = forms.CharField(required=True)

class FormClient(forms.ModelForm):
    class Meta : 
        model = Client
        exclude = ['credit']