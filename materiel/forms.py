from django import forms
from .models import Materiel


class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = [
            'date_entree', 'matricule', 'marque', 'type_materiel', 'type_affectation',
            'emplacement', 'etat', 'stock', 'fournisseur', 'date_sortie',
            'observation', 'service_affecte', 'utilisateur_affecte',
            'kilometrage', 'defaut_panne', 'reparation', 'reference_piece',
            'type_vehicule', 'numero_vehicule', 'date_prochaine_visite',
            'date_mise_circulation', 'type_carburant', 'statut_vehicule', 'divers', 'prix'
        ]
        widgets = {
            'date_entree': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'marque': forms.TextInput(attrs={'class': 'form-control'}),
            'type_materiel': forms.Select(attrs={'class': 'form-control'}),
            'type_affectation': forms.Select(attrs={'class': 'form-control'}),
            'emplacement': forms.TextInput(attrs={'class': 'form-control'}),
            'etat': forms.Select(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'fournisseur': forms.TextInput(attrs={'class': 'form-control'}),
            'date_sortie': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observation': forms.Select(attrs={'class': 'form-control'}),
            'service_affecte': forms.TextInput(attrs={'class': 'form-control'}),
            'utilisateur_affecte': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometrage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'defaut_panne': forms.Select(attrs={'class': 'form-control'}),
            'reparation': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Description des réparations...'}),
            'reference_piece': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Référence de la pièce'}),
            'type_vehicule': forms.Select(attrs={'class': 'form-control'}),
            'numero_vehicule': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de châssis du véhicule'}),
            'date_prochaine_visite': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_mise_circulation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type_carburant': forms.Select(attrs={'class': 'form-control'}),
            'statut_vehicule': forms.Select(attrs={'class': 'form-control'}),
            'divers': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Remarques ou informations libres...'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Champs obligatoires
        self.fields['matricule'].required = True
        self.fields['marque'].required = True
        
        # Champs optionnels
        self.fields['date_entree'].required = False
        self.fields['type_materiel'].required = False
        self.fields['type_affectation'].required = False
        self.fields['emplacement'].required = False
        self.fields['etat'].required = False
        self.fields['stock'].required = False
        self.fields['fournisseur'].required = False
        self.fields['date_sortie'].required = False
        self.fields['observation'].required = False
        self.fields['service_affecte'].required = False
        self.fields['utilisateur_affecte'].required = False
        
        # Champs optionnels avec validation
        self.fields['kilometrage'].required = False
        self.fields['defaut_panne'].required = False
        self.fields['reparation'].required = False
        self.fields['reference_piece'].required = False
        self.fields['type_vehicule'].required = False
        self.fields['numero_vehicule'].required = False
        self.fields['date_prochaine_visite'].required = False
        self.fields['date_mise_circulation'].required = False
        self.fields['type_carburant'].required = False
        self.fields['statut_vehicule'].required = False
        self.fields['divers'].required = False
        self.fields['prix'].required = False
        
        # Labels personnalisés
        self.fields['kilometrage'].label = "Kilométrage"
        self.fields['defaut_panne'].label = "Défaut/Panne"
        self.fields['reparation'].label = "Réparation"
        self.fields['reference_piece'].label = "Référence pièce"
        self.fields['type_vehicule'].label = "Type véhicule"
        self.fields['numero_vehicule'].label = "Numéro de châssis des véhicules"
        self.fields['date_prochaine_visite'].label = "Date de prochaine visite de contrôle technique des véhicules"
        self.fields['date_mise_circulation'].label = "Date de mise en circulation du véhicule"
        self.fields['type_carburant'].label = "Type de carburant"
        self.fields['statut_vehicule'].label = "Statut du véhicule"
        self.fields['divers'].label = "Divers"
        self.fields['prix'].label = "Prix"
        
        # Messages d'aide
        self.fields['kilometrage'].help_text = "Indiquez le kilométrage actuel"
        self.fields['defaut_panne'].help_text = "Type de problème constaté"
        self.fields['reparation'].help_text = "Description des réparations effectuées"
        self.fields['reference_piece'].help_text = "Référence des pièces de rechange"
        self.fields['type_vehicule'].help_text = "Type de véhicule si applicable"
        self.fields['numero_vehicule'].help_text = "Numéro de châssis du véhicule"
        self.fields['date_prochaine_visite'].help_text = "Date de la prochaine visite de contrôle technique"
        self.fields['date_mise_circulation'].help_text = "Date de première mise en circulation du véhicule"
        self.fields['type_carburant'].help_text = "Type de carburant du véhicule"
        self.fields['statut_vehicule'].help_text = "Statut actuel du véhicule"
        self.fields['divers'].help_text = "Remarques ou informations libres"
        self.fields['prix'].help_text = "Prix d'achat ou de réparation"
        
        # Validation personnalisée
        self.fields['kilometrage'].widget.attrs.update({'min': '0'})
        self.fields['prix'].widget.attrs.update({'min': '0'})
    
    def clean_kilometrage(self):
        kilometrage = self.cleaned_data.get('kilometrage')
        if kilometrage is not None and kilometrage < 0:
            raise forms.ValidationError("Le kilométrage ne peut pas être négatif.")
        return kilometrage
    
    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix is not None and prix < 0:
            raise forms.ValidationError("Le prix ne peut pas être négatif.")
        return prix
    
    def clean_numero_vehicule(self):
        numero_vehicule = self.cleaned_data.get('numero_vehicule')
        if numero_vehicule:
            numero_vehicule = numero_vehicule.upper().strip()
        return numero_vehicule
