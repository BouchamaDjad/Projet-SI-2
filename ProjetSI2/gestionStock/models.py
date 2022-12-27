from django.db import models

# Create your models here.

class Prix(models.Model):
    PrixUnite = models.FloatField()
    PrixVente = models.FloatField()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['PrixUnite', 'PrixVente'], name='uniquePrix'
            )
        ]


class Produit(models.Model):
    CodeP = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=30)
    prix = models.ManyToManyField(Prix, through='Stock',through_fields=('produit', 'PrixUnite','PrixVente'))
    def __str__(self):
        return (self.designation)

class Stock(models.Model):
    PrixUnite = models.ForeignKey(Prix,on_delete=models.CASCADE,related_name="StocksPrixU")
    PrixVente = models.ForeignKey(Prix,on_delete=models.CASCADE,related_name="StocksPrixV")
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE,related_name="StockProduits")
    Date = models.DateField(auto_now=True)
    Qtp = models.IntegerField()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['PrixUnite', 'PrixVente','produit'], name='uniqueStock'
            )
        ]
    def __str__(self):
        return (self.designation)