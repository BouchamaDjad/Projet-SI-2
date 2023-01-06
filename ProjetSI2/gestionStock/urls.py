from django.urls import path
from . import views

urlpatterns = [
    path('Fournisseurs/',views.afficher_fournisseur),

    path('BonCommande/',views.créer_bon_commande,name="creationBC"),
    path('BC/<str:filename>/',views.download_file,name="download_file"),

    path('Clients/',views.afficher_client,name = "clients"),

    path('SaisieFacture/',views.saisie_facture, name='saisiefacture'),
    path('ProduitsFacture/',views.produits_facture, name='produitsfacture'),
    path('Facture/<int:pk>/',views.afficher_facture,name="facture"),

    path('Stock/',views.afficher_stock,name='stock'),
    path('Stock/edit/<int:pk>/<int:ppk>',views.ajuster_stock,name='ajusterstock'),

    path('ReglementFactures/',views.reglement_facture, name='reglementfacture'),
    path('ReglerFactures/',views.regler_factures, name='reglerfactures'),
    path('sauv_Reg/<int:pk>',views.sauv_reg,name='sauvreg'),

    path('EntréeStock/',views.entrer_en_stock,name='entrystock'),
    path('SortieStock/',views.sortie_stock,name='sortiestock'),
    
    path('SelectionClient/',views.selection_client,name='selectionclient'),
    path('CreeClientVente/',views.cree_clientV,name='creeclientV'),
    path('CreationVente/<int:pk>/',views.creation_vente,name="creationvente"),
    path('SaisirProduit/<int:v>/',views.saisir_produit,name='saisirproduit'),
    path('QuantiteProduit/<int:v>/<int:s>',views.quantite_produit,name='quantiteproduit'),
    path('PayementVente/<int:v>/',views.payement_vente,name='payementvente'),

    
]