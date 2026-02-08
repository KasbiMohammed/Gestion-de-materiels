# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiel', '0002_materiel_date_prochaine_visite_materiel_defaut_panne_and_more'),
    ]

    operations = [
        # Ajout des nouveaux champs manquants
        migrations.AddField(
            model_name='materiel',
            name='date_mise_circulation',
            field=models.DateField(
                blank=True, 
                help_text='Date de première mise en circulation du véhicule', 
                null=True, 
                verbose_name='Date de mise en circulation du véhicule'
            ),
        ),
        migrations.AddField(
            model_name='materiel',
            name='type_carburant',
            field=models.CharField(
                blank=True, 
                choices=[
                    ('diesel', 'Diesel'),
                    ('essence', 'Essence'),
                    ('hybride', 'Hybride'),
                    ('electrique', 'Électrique'),
                ], 
                help_text='Type de carburant du véhicule', 
                max_length=20, 
                null=True, 
                verbose_name='Type de carburant'
            ),
        ),
        migrations.AddField(
            model_name='materiel',
            name='statut_vehicule',
            field=models.CharField(
                blank=True, 
                choices=[
                    ('en_stock', 'En stock'),
                    ('en_panne', 'En panne'),
                    ('reforme', 'Réformé'),
                ], 
                help_text='Statut actuel du véhicule', 
                max_length=20, 
                null=True, 
                verbose_name='Statut du véhicule'
            ),
        ),
        migrations.AddField(
            model_name='materiel',
            name='divers',
            field=models.TextField(
                blank=True, 
                help_text='Remarques ou informations libres', 
                null=True, 
                verbose_name='Divers'
            ),
        ),
        # Mise à jour des labels des champs existants
        migrations.AlterField(
            model_name='materiel',
            name='numero_vehicule',
            field=models.CharField(
                blank=True, 
                help_text='Numéro de châssis du véhicule', 
                max_length=50, 
                verbose_name='Numéro de châssis des véhicules'
            ),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='date_prochaine_visite',
            field=models.DateField(
                blank=True, 
                help_text='Date de la prochaine visite de contrôle technique', 
                null=True, 
                verbose_name='Date de prochaine visite de contrôle technique des véhicules'
            ),
        ),
        # Rendre les champs optionnels (sauf matricule et marque)
        migrations.AlterField(
            model_name='materiel',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name="Date d'enregistrement"),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='type_materiel',
            field=models.CharField(
                blank=True, 
                choices=[
                    ('informatique', 'Informatique'),
                    ('mobilier', 'Mobilier'),
                    ('vehicule', 'Véhicule'),
                    ('outillage', 'Outillage'),
                    ('telephonie', 'Téléphonie'),
                    ('autre', 'Autre'),
                ], 
                max_length=50, 
                null=True, 
                verbose_name='Type de matériel'
            ),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='type_affectation',
            field=models.CharField(
                blank=True, 
                choices=[
                    ('permanent', 'Permanent'),
                    ('temporaire', 'Temporaire'),
                    ('pret', 'Prêt'),
                    ('stock', 'Stock'),
                ], 
                max_length=50, 
                null=True, 
                verbose_name="Type d'affectation"
            ),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='emplacement',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Emplacement'),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='etat',
            field=models.CharField(
                blank=True, 
                choices=[
                    ('neuf', 'Neuf'),
                    ('bon', 'Bon état'),
                    ('usage', 'Usé'),
                    ('panne', 'En panne'),
                    ('reforme', 'Réformé'),
                ], 
                max_length=20, 
                null=True, 
                verbose_name='État'
            ),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='stock',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Quantité en stock'),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='fournisseur',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Fournisseur'),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='date_reception',
            field=models.DateField(blank=True, null=True, verbose_name='Date de réception'),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='observation',
            field=models.CharField(
                blank=True, 
                choices=[
                    ('marche', 'Marche'),
                    ('arret', 'Arrêt'),
                    ('en_cours', 'En cours'),
                ], 
                default='marche', 
                max_length=20, 
                null=True, 
                verbose_name='Observation'
            ),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='service_affecte',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Service affecté'),
        ),
        migrations.AlterField(
            model_name='materiel',
            name='utilisateur_affecte',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Utilisateur affecté'),
        ),
    ]
