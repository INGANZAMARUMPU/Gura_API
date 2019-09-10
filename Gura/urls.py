from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("connexion", views.connexion),
    path("ajouter/<user>", views.ajouter),
    path("categorie", views.categorie),
    path("modifier/<slug>", views.modifier),
    path("userbyproduct/<acheteur>/<slug>", views.userbyproduct),
    path("usersbyproduct/<slug>/<int:page>", views.usersbyproduct),
    path("supprimer/<user>/<slug>", views.supprimer),
    path("sendmessage", views.sendmessage),
    path("messagerie/<user>/<int:page>", views.messagerie),
    path("produits/<tel>/<int:page>", views.produits),
    path("produitsde/<tel>/<int:page>", views.produitsde),
]