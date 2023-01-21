from django.urls import path
from . import views

urlpatterns = [
    path('AjouterType/',views.ajout_type,name="ajoutType"),
    path('TypesProduits/',views.afficher_type,name='types produit'),
    path('SupprimerType/<int:pk>',views.supprimer_type ,name='DeleteTypes'),
    path('TypesProduits/edit/<int:pk>',views.edit_types,name='editTypes'),

    path('AjouterProduits/',views.ajout_produit,name="ajoutproduit"),
    # modifier
    # suppression

    path('Fournisseurs/',views.afficher_fournisseur,name="fournisseurs"),
    path('ModifierFournisseur/<int:pk>/',views.edit_fournisseur,name="editfournisseur"),
    path('AjouterFournisseur/',views.ajouter_fournisseur,name="ajouterfournisseur"),
    path('SupprimerFournisseur/<int:pk>',views.supprimer_fournisseur,name="supprimerfournisseur"),

    path('BonCommande/',views.créer_bon_commande,name="creationBC"),
    path('BC/<str:filename>/',views.download_file,name="download_file"),

    path('Clients/',views.afficher_client,name = "clients"),
    path('CreationClient/',views.creation_client,name = "creationclient"),
    path('SupprimerClient/<int:pk>',views.supprimer_client,name = "supprimerclient"),
    path('Clients/edit/<int:pk>',views.edit_client,name = "editclient"),

    path('SaisieFacture/',views.saisie_facture, name='saisiefacture'),
    path('ProduitsFacture/<int:pk>/<int:idFr>/<str:date>/',views.produits_facture, name='produitsfacture'),
    path('Facture/<int:pk>/',views.afficher_facture,name="facture"),
    path('listeFactures/',views.liste_factures,name="listefactures"),
    path('detailsFacture/<int:pk>',views.details_facture,name="detailsfacture"),
    path('editFacture/<int:pk>',views.edit_facture,name="editfacture"),
    path('SupprimerFacture/<int:pk>',views.supprimer_facture,name="supprimerfacture"),

    path('Stock/',views.afficher_stock,name='stock'),
    path('Stock/edit/<int:s>',views.ajuster_stock,name='ajusterstock'),

    path('ReglementFactures/',views.reglement_facture, name='reglementfacture'),
    path('ReglerFactures/',views.regler_factures, name='reglerfactures'),
    path('sauv_Reg/<int:pk>/<str:date>',views.sauv_reg,name='sauvreg'),
    path('EntréeStock/',views.entrer_en_stock,name='entrystock'),
    path('SortieStock/',views.sortie_stock,name='sortiestock'),
    path('Déstocker/<int:pk>/',views.déstocker,name='déstocker'),

    path('ReglementVentes/',views.reglement_vente, name='reglementvente'),
    path('ReglerVentes/',views.regler_ventes, name='reglerventes'), 
    path('sauv_RegV/<int:pk>/<str:date>',views.sauv_regV,name='sauvregV'),

    path('SelectionClient/',views.selection_client,name='selectionclient'),
    path('CreeClientVente/',views.cree_clientV,name='creeclientV'),
    path('SaisirProduit/<int:pk>/',views.saisir_produit,name='saisirproduit'),
    path('SaisirProduit2/<int:v>/',views.saisir_produit2,name='saisirproduit2'),
    path('QuantiteProduit/<int:pk>/<int:s>',views.quantite_produit,name='quantiteproduit'),
    path('QuantiteProduit2/<int:v>/<int:s>',views.quantite_produit2,name="quantiteproduit2"),
    path('PayementVente/<int:v>/',views.payement_vente,name='payementvente'),

    path('Stats/',views.stats,name='stats'),
    path('StatsAchats/',views.statsAchat,name='statsAchats'), 
]