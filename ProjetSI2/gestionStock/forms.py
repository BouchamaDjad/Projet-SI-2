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

class TypeProduitChoiceField(forms.ModelChoiceField):
    class Meta:
        model=TypeProduit
        field=['designation'] 
    
class FiltreForm(forms.Form):
    date = forms.DateField(required=False)
    type = TypeProduitChoiceField(TypeProduit.objects.all(),required=False)
    quantité = forms.IntegerField(label_suffix='<=',required=False)
    designation_produit = forms.CharField(required=False)