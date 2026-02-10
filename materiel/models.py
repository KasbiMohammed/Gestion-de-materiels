from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


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
    
    OBSERVATION_CHOICES = [
        ('marche', 'Marche'),
        ('arret', 'Arrêt'),
        ('en_cours', 'En cours'),
    ]
    
    DEFAUT_PANNE_CHOICES = [
        ('defaut', 'Défaut'),
        ('panne', 'Panne'),
    ]
    
    TYPE_VEHICULE_CHOICES = [
        ('voiture', 'Voiture'),
        ('camion', 'Camion'),
        ('moto', 'Moto'),
        ('utilitaire', 'Utilitaire'),
        ('engin', 'Engin de chantier'),
        ('autre', 'Autre'),
    ]
    
    TYPE_CARBURANT_CHOICES = [
        ('diesel', 'Diesel'),
        ('essence', 'Essence'),
        ('hybride', 'Hybride'),
        ('electrique', 'Électrique'),
    ]
    
    STATUT_VEHICULE_CHOICES = [
        ('en_stock', 'En stock'),
        ('en_panne', 'En panne'),
        ('reforme', 'Réformé'),
    ]

    date_entree = models.DateField("Date d'entrée", null=True, blank=True)
    matricule = models.CharField("Matricule", max_length=50, unique=True)
    marque = models.CharField("Marque", max_length=100)
    type_materiel = models.CharField("Type de matériel", max_length=50, choices=TYPE_MATERIEL_CHOICES, null=True, blank=True)
    type_affectation = models.CharField("Type d'affectation", max_length=50, choices=TYPE_AFFECTATION_CHOICES, null=True, blank=True)
    emplacement = models.CharField("Emplacement", max_length=100, null=True, blank=True)
    etat = models.CharField("État", max_length=20, choices=ETAT_CHOICES, null=True, blank=True)
    stock = models.IntegerField("Quantité en stock", default=1, null=True, blank=True)
    fournisseur = models.CharField("Fournisseur", max_length=100, null=True, blank=True)
    date_sortie = models.DateField("Date de sortie", null=True, blank=True)
    observation = models.CharField("Observation", max_length=20, choices=OBSERVATION_CHOICES, default='marche', null=True, blank=True)
    service_affecte = models.CharField("Service affecté", max_length=100, null=True, blank=True)
    utilisateur_affecte = models.CharField("Utilisateur affecté", max_length=100, null=True, blank=True)
    
    # Nouveaux champs
    kilometrage = models.DecimalField("Kilométrage", max_digits=10, decimal_places=2, null=True, blank=True, help_text="Indiquez le kilométrage actuel")
    defaut_panne = models.CharField("Défaut/Panne", max_length=10, choices=DEFAUT_PANNE_CHOICES, blank=True, help_text="Type de problème constaté")
    reparation = models.TextField("Réparation", blank=True, help_text="Description des réparations effectuées")
    reference_piece = models.CharField("Référence pièce", max_length=100, blank=True, help_text="Référence des pièces de rechange")
    type_vehicule = models.CharField("Type véhicule", max_length=20, choices=TYPE_VEHICULE_CHOICES, blank=True, help_text="Type de véhicule si applicable")
    numero_vehicule = models.CharField("Numéro de châssis des véhicules", max_length=50, blank=True, help_text="Numéro de châssis du véhicule")
    date_prochaine_visite = models.DateField("Date de prochaine visite de contrôle technique des véhicules", null=True, blank=True, help_text="Date de la prochaine visite de contrôle technique")
    date_mise_circulation = models.DateField("Date de mise en circulation du véhicule", null=True, blank=True, help_text="Date de première mise en circulation du véhicule")
    type_carburant = models.CharField("Type de carburant", max_length=20, choices=TYPE_CARBURANT_CHOICES, null=True, blank=True, help_text="Type de carburant du véhicule")
    statut_vehicule = models.CharField("Statut du véhicule", max_length=20, choices=STATUT_VEHICULE_CHOICES, null=True, blank=True, help_text="Statut actuel du véhicule")
    divers = models.TextField("Divers", null=True, blank=True, help_text="Remarques ou informations libres")
    prix = models.DecimalField("Prix", max_digits=10, decimal_places=2, null=True, blank=True, help_text="Prix d'achat ou de réparation")
    
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


class Visite(models.Model):
    TYPE_VISITE_CHOICES = [
        ('entretien', 'Entretien'),
        ('controle_technique', 'Contrôle Technique'),
        ('inspection', 'Inspection'),
        ('reparation', 'Réparation'),
        ('prevention', 'Visite Préventive'),
        ('autre', 'Autre'),
    ]
    
    TYPE_CONTROLE_CHOICES = [
        ('huile_moteur', 'Huile moteur'),
        ('filtres', 'Filtres'),
        ('freins', 'Freins'),
        ('pneus', 'Pneus'),
        ('batterie', 'Batterie'),
        ('systeme_electronique', 'Système électronique'),
        ('climatisation', 'Climatisation'),
        ('suspension', 'Suspension'),
        ('echappement', 'Échappement'),
        ('transmission', 'Transmission'),
        ('eclairage', 'Éclairage'),
        ('autre', 'Autre'),
    ]
    
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE, related_name='visites')
    date_visite = models.DateField("Date de visite")
    type_visite = models.CharField("Type de visite", max_length=20, choices=TYPE_VISITE_CHOICES)
    kilometrage = models.DecimalField("Kilométrage", max_digits=10, decimal_places=2, null=True, blank=True)
    responsable = models.CharField("Responsable/Mécanicien", max_length=100, null=True, blank=True)
    observations = models.TextField("Observations", null=True, blank=True)
    cout = models.DecimalField("Coût", max_digits=10, decimal_places=2, null=True, blank=True)
    prochaine_visite = models.DateField("Prochaine visite prévue", null=True, blank=True)
    
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    updated_at = models.DateTimeField("Date de mise à jour", auto_now=True)
    
    class Meta:
        verbose_name = "Visite"
        verbose_name_plural = "Visites"
        ordering = ['-date_visite']
    
    def __str__(self):
        return f"{self.materiel.matricule} - {self.get_type_visite_display()} ({self.date_visite})"


class ControleVisite(models.Model):
    visite = models.ForeignKey(Visite, on_delete=models.CASCADE, related_name='controles')
    type_controle = models.CharField("Type de contrôle", max_length=30, choices=Visite.TYPE_CONTROLE_CHOICES)
    effectue = models.BooleanField("Contrôle effectué", default=True)
    details = models.TextField("Détails du contrôle", null=True, blank=True)
    pieces_changees = models.TextField("Pièces changées", null=True, blank=True)
    
    class Meta:
        verbose_name = "Contrôle de visite"
        verbose_name_plural = "Contrôles de visite"
    
    def __str__(self):
        return f"{self.visite} - {self.get_type_controle_display()}"
