from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

class Profil(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    avatar = models.ImageField(null=True, blank=True, upload_to="profils/")
    tel = models.CharField(max_length=15, unique=True, verbose_name='numero de téléphone')
    adresse = models.CharField(max_length=15, null=True, verbose_name='adresse')
    ville = models.CharField(max_length=15, null=True, verbose_name='ville')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Message(models.Model):
    source = models.ForeignKey("Profil", on_delete=models.CASCADE, related_name='source', verbose_name="client")
    date = models.DateTimeField(default=timezone.now)
    lu = models.BooleanField(default=False)
    message = models.TextField()
    destination = models.ForeignKey("Profil", on_delete=models.CASCADE, related_name='destination', verbose_name="vendeur du produit")
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)

class Categorie(models.Model):
    categorie = models.CharField(null=False, max_length=30)

    def __str__(self):
        return f"{self.categorie}"
    
class Produit(models.Model):
    titre = models.CharField(max_length=30, verbose_name="titre du produit")
    categorie = models.ForeignKey("Categorie", null=True, on_delete=models.SET_NULL)
    photo = models.ImageField(upload_to="covers/")
    description = models.TextField(verbose_name="description du produit")
    prix = models.IntegerField(verbose_name="prix")
    vendeur = models.ForeignKey("Profil", verbose_name="vendeur du produit", on_delete=models.CASCADE)
    vendu = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, default="sans", max_length=30)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titre+" "+str(self.vendeur))
        super(Produit, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.titre} de {self.vendeur}"
