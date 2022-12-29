from django.urls import path
from . import views

urlpatterns = [
    path('Clients/',views.afficher_client),
    path('Fournisseurs/',views.afficher_fournisseur),
]