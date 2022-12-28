from django.contrib import admin
from .models import Prix,Stock,Produit,Composer,Vente,Client,ReglementVente
from .models import Fournisseur,Facture,TypeProduit,ReglementFacture,Avoir,EntreeStock,SortieStock
# Register your models here.
admin.site.register(Produit)
admin.site.register(Stock)
admin.site.register(Prix)
admin.site.register(Composer)
admin.site.register(Vente)
admin.site.register(Client)
admin.site.register(ReglementVente)
admin.site.register(ReglementFacture)
admin.site.register(Fournisseur)
admin.site.register(Facture)
admin.site.register(TypeProduit)
admin.site.register(Avoir)
admin.site.register(EntreeStock)
admin.site.register(SortieStock)