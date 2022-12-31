from datetime import datetime
from django import forms
from .models import *

class MultiProduitField(forms.ModelMultipleChoiceField):
    qt = forms.IntegerField()
    class Meta:
        model = Produit
        field = ('codeP','designation')

class FournisseurChoiceField(forms.ModelChoiceField):
    class Meta:
        model = Fournisseur
        field = ('nom','prenom')

class BCForm(forms.Form):
    date = forms.DateTimeField(initial = datetime.now)
    fournisseur = FournisseurChoiceField(Fournisseur.objects.all())
    produits = MultiProduitField(Produit.objects.all())


