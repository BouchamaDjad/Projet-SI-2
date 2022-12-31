from django.urls import path
from . import views

urlpatterns = [
    path('Clients/',views.afficher_client),
    path('Fournisseurs/',views.afficher_fournisseur),
    path('BonCommande/',views.créer_bon_commande,name="creationBC"),
    path('BonCommande/<str:filename>/',views.download_file,name="download_file"),
]