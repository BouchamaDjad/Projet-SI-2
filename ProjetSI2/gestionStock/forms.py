from django.db.models import fields
from django import forms
from .models import Facture,Produit,Prix,Avoir

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ('numero','date','fournisseur')
        widgets = {
            'date':forms.DateInput( attrs= {'type':'date'})
            
        }

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ('numero','date','fournisseur')
        widgets = {
            'date':forms.DateInput( attrs= {'type':'date'})
            
        }

class produitFacture(forms.ModelForm):
    class Meta :
        model = Produit
        fields = ['designation']

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
    