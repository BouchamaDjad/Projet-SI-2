from django.urls import path
from . import views

urlpatterns = [
    path('Clients/',views.afficher_client,name = "clients"),
    path('SaisieFacture/',views.saisie_facture, name='saisiefacture'),
    path('ProduitsFacture/',views.produits_facture, name='produitsfacture'),
]