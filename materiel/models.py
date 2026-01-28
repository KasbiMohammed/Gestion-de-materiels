from django.db import models
from django.contrib.auth.models import User


class Materiel(models.Model):
    ETAT_CHOICES = [
        ('neuf', 'Neuf'),
        ('bon', 'Bon état'),
        ('usage', 'Usé'),
        ('panne', 'En panne'),
        ('reforme', 'Réformé'),
    ]
    
    TYPE_MATERIEL_CHOICES = [
        ('informatique', 'Informatique'),
        ('mobilier', 'Mobilier'),
        ('vehicule', 'Véhicule'),
        ('outillage', 'Outillage'),
        ('telephonie', 'Téléphonie'),
        ('autre', 'Autre'),
    ]
    
    TYPE_AFFECTATION_CHOICES = [
        ('permanent', 'Permanent'),
        ('temporaire', 'Temporaire'),
        ('pret', 'Prêt'),
        ('stock', 'Stock'),
    ]

    date = models.DateField("Date d'enregistrement")
    matricule = models.CharField("Matricule", max_length=50, unique=True)
    marque = models.CharField("Marque", max_length=100)
    type_materiel = models.CharField("Type de matériel", max_length=50, choices=TYPE_MATERIEL_CHOICES)
    type_affectation = models.CharField("Type d'affectation", max_length=50, choices=TYPE_AFFECTATION_CHOICES)
    emplacement = models.CharField("Emplacement", max_length=100)
    etat = models.CharField("État", max_length=20, choices=ETAT_CHOICES)
    stock = models.IntegerField("Quantité en stock", default=1)
    fournisseur = models.CharField("Fournisseur", max_length=100)
    date_reception = models.DateField("Date de réception")
    observation = models.TextField("Observation", blank=True)
    service_affecte = models.CharField("Service affecté", max_length=100)
    utilisateur_affecte = models.CharField("Utilisateur affecté", max_length=100)
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    updated_at = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Matériel"
        verbose_name_plural = "Matériels"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.matricule} - {self.marque} ({self.type_materiel})"

    def get_absolute_url(self):
        return f"/materiel/{self.id}/"
