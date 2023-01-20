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
            'date':forms.DateInput( attrs= {'type':'date','class':"form-control date"}),
            'numero':forms.NumberInput( attrs= {'class':"form-control"}),
            'fournisseur':forms.Select( attrs= {'class':"form-control"}),
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
        widgets = {
            "PrixUnite" : forms.NumberInput(attrs={"class":"form-control","style": "width:fit-content"}),
            "PrixVente" : forms.NumberInput(attrs={"class":"form-control","style": "width:fit-content"}),
        }


class qtAchete(forms.ModelForm):
    class Meta :
        model = Avoir
        fields = ['qta']
        labels = {
            'qta':'Quantite',
        }
        widgets = {
            'qta':forms.NumberInput(attrs={"class":"form-control","style": "width:fit-content"})
        }

class OptionFacture(forms.Form):
    payer = forms.BooleanField(label='payer',required=False)
    remise = forms.FloatField(label = 'Remise (%)',initial=0)

class reglementFacture(forms.ModelForm):
    class Meta:
        model = ReglementFacture
        fields = ['date']
        widgets = {
            'date':forms.DateInput( attrs= {'type':'date','style':'display:block'})
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
    designation_produit = forms.CharField(required=False)
    date = forms.DateField(required=False)
    type = TypeProduitChoiceField(TypeProduit.objects.all(),required=False)
    quantité = forms.IntegerField(label_suffix='<=',required=False)

class StockForm(forms.Form):
    choice = [(p.CodeP,p.designation) for p in Produit.objects.all()]
    codeP = forms.ChoiceField(choices=choice,label="CodeP", widget=forms.Select(attrs={"class":"form-control"}))
    prixHT = forms.FloatField(label="PrixHT",widget=forms.NumberInput(attrs={"class":"form-control"}))
    prixVente =  forms.FloatField(label="PrixVente",widget=forms.NumberInput(attrs={"class":"form-control"}))
    Qtp = forms.IntegerField(label="Quantité",widget=forms.NumberInput(attrs={"class":"form-control"}))

class EntrerStockForm(forms.Form):
    min = Produit.objects.latest('CodeP').CodeP+1
    CodeP = forms.IntegerField(initial=min,widget=forms.NumberInput(attrs={"class":"form-control","min":min}) )
    Designation  = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    Type = TypeProduitChoiceField(TypeProduit.objects.all(),widget=forms.Select(attrs={"class":"form-control"}))
    Date = forms.DateField(initial=datetime.today(),widget=forms.DateInput(attrs={"class":"form-control","style":"display:block"}))
    Quantité = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}))

class SortieStockForm(forms.ModelForm):
    class Meta:
        model = SortieStock
        fields = ["motif","qt"]
        widgets = {
            "motif":forms.TextInput(attrs={"class":"form-control"}),
            "qt":forms.NumberInput(attrs={"class":"form-control"})
        }

class FiltreClient(forms.Form):
   nom = forms.CharField(required=True)

class FiltreProduit(forms.Form):
   nom = forms.CharField(required=True)

class FormClient(forms.ModelForm):
    class Meta : 
        model = Client
        exclude = ['credit']
    def __init__(self, *args, **kwargs):
        super(FormClient, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class reglementVente(forms.ModelForm):
    class Meta:
        model = ReglementVente
        fields = ['date']
        widgets = {
            'date':forms.DateInput( attrs= {'type':'date','style':'display:block'})
        }

class SelectionClient(forms.Form):
    choices = []
    clients = Client.objects.all()
    for f in clients :
        choices.append((f.id,f'{f.nom} {f.prenom}'))
    Client = forms.ChoiceField(choices = tuple(choices))