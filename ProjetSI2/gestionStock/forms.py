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
    def __init__(self,*args, **kwargs):
        self._choixF = kwargs.pop('choixF', None)
        super().__init__(*args, **kwargs)
        self.fields['Fournisseur'].choices = self._choixF
    
    Fournisseur = forms.ChoiceField(choices = ())

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

class FormFournisseur(forms.ModelForm):
    class Meta : 
        model = Fournisseur
        exclude = ['solde']
    def __init__(self, *args, **kwargs):
        super(FormFournisseur, self).__init__(*args, **kwargs)
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
    def __init__(self,*args, **kwargs):
        self._choixC = kwargs.pop('choixC', None)
        super(SelectionClient, self).__init__(*args, **kwargs)
        self.fields['Client'].choices =self._choixC
    Client = forms.ChoiceField(choices = ())

class FormType(forms.ModelForm):
    class Meta:
        model = TypeProduit
        fields= ["designation"]
    def __init__(self, *args, **kwargs):
        super(FormType, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class FormProduit(forms.ModelForm):
    class Meta:
        model = Produit
        fields= ["designation","typeP"]
    def __init__(self, *args, **kwargs):
        super(FormProduit, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'  

class FormFacture(forms.ModelForm):
    class Meta:
        model = Facture
        exclude = ["numero"]
    def __init__(self, *args, **kwargs):
        super(FormFacture, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class FormRegF(forms.ModelForm):
    class Meta:
        model = ReglementFacture
        exclude = ["facture"]
    def __init__(self, *args, **kwargs):
        super(FormRegF, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class FormRegV(forms.ModelForm):
    class Meta:
        model = ReglementVente
        exclude = ["vente"]
    def __init__(self, *args, **kwargs):
        super(FormRegV, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class FormVente(forms.ModelForm):
    class Meta:
        model = Vente
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(FormVente, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'