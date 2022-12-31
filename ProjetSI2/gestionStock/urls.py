from django.urls import path
from . import views

urlpatterns = [
    path('Fournisseurs/',views.afficher_fournisseur),
    path('BonCommande/',views.créer_bon_commande,name="creationBC"),
    path('BonCommande/<str:filename>/',views.download_file,name="download_file"),
    path('Clients/',views.afficher_client,name = "clients"),
    path('SaisieFacture/',views.saisie_facture, name='saisiefacture'),
    path('ProduitsFacture/',views.produits_facture, name='produitsfacture'),
]