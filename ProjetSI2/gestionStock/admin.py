from django.contrib import admin
from .models import Prix,Stock,Produit

# Register your models here.
admin.site.register(Produit)
admin.site.register(Stock)
admin.site.register(Prix)