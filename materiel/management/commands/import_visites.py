from django.core.management.base import BaseCommand
from django.utils import timezone
from materiel.models import Materiel, Visite, ControleVisite
import re

class Command(BaseCommand):
    help = 'Importe les données de réparations existantes dans le système de visites'

    def handle(self, *args, **options):
        self.stdout.write('Début de l\'importation des visites...')
        
        # Récupérer tous les véhicules avec des données de réparation
        vehicules_avec_reparations = Materiel.objects.filter(
            type_materiel='vehicule'
        ).exclude(
            reparation__isnull=True
        ).exclude(
            reparation=''
        )
        
        visites_crees = 0
        controles_crees = 0
        
        for vehicule in vehicules_avec_reparations:
            self.stdout.write(f'Traitement du véhicule: {vehicule.matricule}')
            
            # Créer une visite à partir des données de réparation
            visite = Visite.objects.create(
                materiel=vehicule,
                date_visite=vehicule.updated_at.date() if vehicule.updated_at else timezone.now().date(),
                type_visite='reparation',  # Par défaut, on considère que c'est une réparation
                kilometrage=vehicule.kilometrage,
                observations=vehicule.reparation,
                cout=vehicule.prix,
                created_at=vehicule.updated_at or timezone.now(),
                updated_at=vehicule.updated_at or timezone.now()
            )
            
            visites_crees += 1
            
            # Analyser les détails de réparation pour créer des contrôles
            if vehicule.reparation:
                controles = self.analyser_reparation(vehicule.reparation)
                for controle_data in controles:
                    ControleVisite.objects.create(
                        visite=visite,
                        type_controle=controle_data['type'],
                        effectue=True,
                        details=controle_data['details'],
                        pieces_changees=controle_data.get('pieces', '')
                    )
                    controles_crees += 1
            
            # Ajouter un contrôle pour la référence de pièce si disponible
            if vehicule.reference_piece:
                ControleVisite.objects.create(
                    visite=visite,
                    type_controle='autre',
                    effectue=True,
                    details='Pièce de rechange utilisée',
                    pieces_changees=vehicule.reference_piece
                )
                controles_crees += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Importation terminée! {visites_crees} visites et {controles_crees} contrôles créés.'
            )
        )
    
    def analyser_reparation(self, texte_reparation):
        """Analyse le texte de réparation pour extraire les types de contrôles"""
        controles = []
        texte = texte_reparation.lower()
        
        # Mots-clés pour chaque type de contrôle
        mots_cles = {
            'huile_moteur': ['huile', 'vidange', 'moteur huile', 'huile moteur'],
            'filtres': ['filtre', 'filtres', 'filter', 'filtrage'],
            'freins': ['frein', 'freins', 'plaquette', 'disque', 'freinage'],
            'pneus': ['pneu', 'pneus', 'roue', 'roues', 'pneumatique'],
            'batterie': ['batterie', 'batteries', 'accumulateur', 'charge'],
            'systeme_electronique': ['électronique', 'electronique', 'calculateur', 'capteur', 'système'],
            'climatisation': ['clim', 'climatisation', 'air conditionné', 'climatiseur'],
            'suspension': ['suspension', 'amortisseur', 'ressort', 'suspensions'],
            'echappement': ['échappement', 'pot', 'silencieux', 'échappement'],
            'transmission': ['boîte', 'transmission', 'embrayage', 'vitesses'],
            'eclairage': ['feu', 'phares', 'éclairage', 'ampoule', 'feux']
        }
        
        # Chercher les mots-clés dans le texte
        for type_controle, keywords in mots_cles.items():
            for keyword in keywords:
                if keyword in texte:
                    # Extraire la phrase contenant le mot-clé
                    phrases = texte.split('.')
                    for phrase in phrases:
                        if keyword in phrase:
                            controles.append({
                                'type': type_controle,
                                'details': phrase.strip(),
                                'pieces': ''
                            })
                            break
                    break
        
        # Si aucun contrôle spécifique n'est trouvé, créer un contrôle "autre"
        if not controles:
            controles.append({
                'type': 'autre',
                'details': texte_reparation,
                'pieces': ''
            })
        
        return controles
