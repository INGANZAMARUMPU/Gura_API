from django.shortcuts import HttpResponse
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Q
from django.contrib.auth.models import User
from json import dumps as jsonify

def connexion(request):
    email = request.GET["email"]
    password = request.GET["password"]
    user = User.objects.get(email=email)#pas
    utilisateur = []
    
    if(user.check_password(password)):
        profil = Profil.objects.get(user=user)

        data = {
        	"id": profil.id,
        	"nom" : user.first_name,
        	"prenom" : user.last_name,
        	"email" : user.email,
        	"tel" : profil.tel,
        	"addresse" : profil.adresse,
        	"ville" : profil.ville,
        	"avatar" : profil.avatar.url
        }
        utilisateur.append(data)
        json = jsonify(utilisateur)
        return HttpResponse(json , content_type="application/json")
    return HttpResponse(f"erreur")


def ajouter(request, user):
    user = User.objects.get(username=user)
    vendeur = Profil.objects.get(user=user)
    categorie = Categorie.objects.get(categorie=request.POST["categorie"])
    titre = request.POST["titre"]
    photo = request.POST["photo"]
    description = request.POST["description"]
    prix = request.POST["prix"]

    Produit(vendeur=vendeur, categorie=categorie, titre=titre, \
        photo=photo, description=description, prix=prix).save()
    # json = serialize("json", [user])
    return HttpResponse(None, content_type="application/json")

def modifier(request, slug):
    user = User.objects.get(username=user)
    vendeur = Profil.objects.get(user=user)
    categorie = Categorie.objects.get(categorie=request.POST["categorie"])
    titre = request.POST["titre"]
    photo = request.POST["photo"]
    description = request.POST["description"]
    prix = request.POST["prix"]
    produit = Produit.objects.get(slug=slug)

    if produit.vendeur==vendeur:
        produit.categorie = categorie
        produit.titre = titre
        produit.photo = photo
        produit.description = description
        produit.prix = prix
        produit.save()

    json = serialize("json", [produit])
    return HttpResponse(json, content_type="application/json")

def categorie(request):
    cat = Categorie.objects.all()
    json = serialize("json", [cat])
    return HttpResponse(json, content_type="application/json")

def supprimer(request, user, slug):
    user = User.objects.get(username=user)
    produit = Produit.objects.filter(slug=slug)
    if produit.vendeur.user == user:
        produit.delete()
    json = serialize("json", [produit])
    return HttpResponse(None, content_type="application/json")

def sendmessage(request):
    source = Profil.objects.get(tel=request.GET["source"])
    destination = Profil.objects.get(tel=request.GET["destination"])
    texte = request.GET["message"]
    produit = Produit.objects.get(slug=request.GET["slug"])
    sms = Message(source=source, destination=destination, message=texte, produit=produit)
    sms.save()
    json = serialize("json", [sms])
    return HttpResponse("json", content_type="application/json")

def messagerie(request, user, page):
    profil = Profil.objects.get(tel=user)
    products = []
    p = Message.objects.filter(Q(source=profil) | Q(destination=profil))
    produit = p.filter(lu=False).values_list("produit").distinct()

    pages = Paginator(produit, 8, orphans=3)
    if page<1 or page>pages.num_pages:
        products = jsonify(products)
        return HttpResponse(products, content_type='application/json')
    for x in pages.page(page):
        product = Produit.objects.get(id=x[0])
        data = {
            "titre" : product.titre,
            "prix" : product.prix, 
            "photo" : product.photo.url,
            "slug" : product.slug,
            "vendeur" : product.vendeur.tel,
            "details": product.description
        }
        products.append(data)
    products = jsonify(products)
    return HttpResponse(products, content_type='application/json')
    
def usersbyproduct(request, slug, page):
    produit = Produit.objects.get(slug=slug)
    users = []        
    p = Message.objects.filter(produit=produit)
    produit = p.values_list("source").distinct()

    pages = Paginator(produit, 8, orphans=3)
    if page<1 or page>pages.num_pages:
        users = jsonify(users)
        return HttpResponse(users, content_type='application/json')
    for x in pages.page(page):
        user = Profil.objects.get(id=x[0])
        message = Message.objects.filter(source=user).order_by('-date')[0]
        data = {
            "username" : user.user.username,
            "tel" : user.tel, 
            "message" : message.message,
            "lu" : message.lu
        }
        users.append(data)
    users = jsonify(users)
    return HttpResponse(users, content_type='application/json')

def userbyproduct(request, acheteur, slug):
    users = []        
    product = Produit.objects.get(slug=slug)
    vendeur = product.vendeur
    acheteur = Profil.objects.get(tel=acheteur)

    message = Message.objects.filter(
        Q(Q(source=vendeur) & Q(destination=acheteur)|
            Q(source=acheteur) & Q(destination=vendeur))&
        Q(produit=product))
    # where source != destination
    message = message.order_by('-date')[0]
    data = {
        "username" : vendeur.user.username,
        "tel" : vendeur.tel, 
        "message" : message.message,
        "lu" : message.lu
    }
    users.append(data)
    users = jsonify(users)
    return HttpResponse(users, content_type='application/json')

def produits(request, tel, page):
    products = []
    profil = Profil.objects.get(tel=tel)
    P = Produit.objects.filter(Q(vendu=False) & ~Q(vendeur=profil))
    pages = Paginator(P, 8, orphans=3)
    if page<1 or page>pages.num_pages:
	    products = jsonify(products)
	    return HttpResponse(products, content_type='application/json')
    for x in pages.page(page):
    	data = {
    		"titre" : x.titre,
    		"prix" : x.prix, 
    		"photo" : x.photo.url,
    		"slug" : x.slug,
    		"vendeur" : x.vendeur.tel,
    		"details": x.description
    	}
    	products.append(data)
    products = jsonify(products)
    return HttpResponse(products, content_type='application/json')

def produitsde(request, tel, page):
    products = []
    profil = Profil.objects.get(tel=tel)
    P = Produit.objects.filter(vendu=False, vendeur=profil)
    pages = Paginator(P, 8, orphans=3)
    if page<1 or page>pages.num_pages:
	    products = jsonify(products)
	    return HttpResponse(products, content_type='application/json')

    for x in pages.page(page):
    	data = {
    		"titre" : x.titre,
    		"prix" : x.prix, 
    		"photo" : x.photo.url,
    		"slug" : x.slug,
    		"vendeur" : x.vendeur.tel,
    		"details": x.description
    	}
    	products.append(data)
    products = jsonify(products)
    return HttpResponse(products, content_type='application/json')