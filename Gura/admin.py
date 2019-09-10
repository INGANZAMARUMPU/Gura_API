from django.contrib import admin
from .models import *

class MessageAdmin(admin.ModelAdmin):
    list_display = ("source", "date", "message", "lu", "produit")
    list_filter = ("source", "date", "message", "lu", "produit")
    search_fields = ("source", "date", "message", "lu", "produit")

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'photo', 'description', 'prix', 'vendeur', 'vendu')
    list_filter = list_display
    search_fields = list_display
    prepopulated_fields = {'slug': ('titre', )}

class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', "tel")
    list_filter = ('user', 'avatar', "tel")
    search_fields = ('user', 'avatar', "tel")
        
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("categorie",)
    list_filter = ("categorie",)
    search_fields = ("categorie",)

admin.site.register(Message, MessageAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Profil, ProfilAdmin)