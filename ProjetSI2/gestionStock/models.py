from django.db import models

# Create your models here.

class Prix(models.Model):
    PrixUnite = models.FloatField()
    PrixVente = models.FloatField()
    def __str__(self):
        return f'{self.PrixUnite}/{self.PrixVente}'

class TypeProduit(models.Model):
    designation = models.CharField(max_length=20)
    def __str__(self):
        return (self.designation)

class Produit(models.Model):
    CodeP = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=30)
    prix = models.ManyToManyField(Prix, through='Stock',through_fields=('produit','Prix'))
    typeP = models.ForeignKey(TypeProduit,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return (self.designation)

class Stock(models.Model):
    Prix = models.ForeignKey(Prix,on_delete=models.CASCADE,related_name="StocksPrix")
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE,related_name="StockProduits")
    Date = models.DateField(auto_now=True)
    Qtp = models.IntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['Prix','produit'], name='uniqueStock'
            )
        ]

class EntreeStock(models.Model):
    date = models.DateField(auto_now=True)
    qt = models.IntegerField()
    produit = models.ForeignKey(Produit,on_delete=models.SET_NULL,null=True)

class SortieStock(models.Model):
    date = models.DateField(auto_now=True)
    motif = models.CharField(max_length=30)
    produit = models.ForeignKey(Produit,on_delete=models.SET_NULL,null=True)

class Client(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50,blank = True)
    phone = models.CharField(max_length=10,blank=True,null=True)
    credit = models.FloatField(default=0,blank=True)
    def __str__(self):
        return f'{self.nom} {self.prenom}'

class Vente(models.Model):
    Date = models.DateField(auto_now=True)
    client = models.ForeignKey(Client,null=True,on_delete=models.SET_NULL)
    restant = models.FloatField()
    def __str__(self):
        return f'{self.id} {self.Date}'
   

class Composer(models.Model):
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
    prix = models.ForeignKey(Prix,on_delete=models.CASCADE)
    vente = models.ForeignKey(Vente,on_delete=models.CASCADE)
    QtV = models.IntegerField()
    def __str__(self):
        return f'{self.produit.designation} {self.prix.PrixVente} {self.QtV}'

class ReglementVente(models.Model):
    date = models.DateField(auto_now=True)
    sommeAjoute = models.FloatField()
    vente = models.ForeignKey(Vente,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.vente} -  {self.sommeAjoute} -  {self.date}'

class Fournisseur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50,blank = True)
    phone = models.CharField(max_length=10,blank=True,null=True)
    solde = models.FloatField(default=0,blank=True)
    def __str__(self):
        return f'{self.nom} {self.prenom}'


class Facture(models.Model):
    numero = models.IntegerField(primary_key=True)
    date = models.DateField()
    remise = models.FloatField(default=0)
    sommeRestante = models.FloatField(default=0)
    fournisseur = models.ForeignKey(Fournisseur,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return f'{self.date} {self.fournisseur.nom}'

class Avoir(models.Model):
    qta = models.IntegerField()
    facture = models.ForeignKey(Facture,on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
    prix = models.ForeignKey(Prix,on_delete=models.CASCADE)

class ReglementFacture(models.Model):
    date = models.DateField(editable=True)
    sommeAjoute = models.FloatField(default=0)
    facture = models.ForeignKey(Facture,on_delete=models.SET_NULL,null=True)




