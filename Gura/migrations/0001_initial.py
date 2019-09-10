# Generated by Django 2.2.3 on 2019-09-02 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorie', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='profils/')),
                ('tel', models.CharField(max_length=15, verbose_name='numero de téléphone')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=30, verbose_name='titre du produit')),
                ('photo', models.ImageField(upload_to='covers/')),
                ('description', models.TextField(verbose_name='description du produit')),
                ('prix', models.IntegerField(verbose_name='prix')),
                ('vendu', models.BooleanField(default=False)),
                ('slug', models.SlugField(default='sans', max_length=30, unique=True)),
                ('categorie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Gura.Categorie')),
                ('vendeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gura.Profil', verbose_name='vendeur du produit')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('lu', models.BooleanField(default=False)),
                ('message', models.TextField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='Gura.Profil', verbose_name='vendeur du produit')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gura.Produit')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='Gura.Profil', verbose_name='client')),
            ],
        ),
    ]
