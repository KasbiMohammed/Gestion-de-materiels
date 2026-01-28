from django import forms
from .models import Materiel


class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = [
            'date', 'matricule', 'marque', 'type_materiel', 'type_affectation',
            'emplacement', 'etat', 'stock', 'fournisseur', 'date_reception',
            'observation', 'service_affecte', 'utilisateur_affecte',
            'kilometrage', 'defaut_panne', 'reparation', 'reference_piece',
            'type_vehicule', 'numero_vehicule', 'date_prochaine_visite', 'prix'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'marque': forms.TextInput(attrs={'class': 'form-control'}),
            'type_materiel': forms.Select(attrs={'class': 'form-control'}),
            'type_affectation': forms.Select(attrs={'class': 'form-control'}),
            'emplacement': forms.TextInput(attrs={'class': 'form-control'}),
            'etat': forms.Select(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'fournisseur': forms.TextInput(attrs={'class': 'form-control'}),
            'date_reception': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observation': forms.Select(attrs={'class': 'form-control'}),
            'service_affecte': forms.TextInput(attrs={'class': 'form-control'}),
            'utilisateur_affecte': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometrage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'defaut_panne': forms.Select(attrs={'class': 'form-control'}),
            'reparation': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Description des réparations...'}),
            'reference_piece': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Référence de la pièce'}),
            'type_vehicule': forms.Select(attrs={'class': 'form-control'}),
            'numero_vehicule': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro d\'immatriculation'}),
            'date_prochaine_visite': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Champs obligatoires
        self.fields['date'].required = True
        self.fields['matricule'].required = True
        self.fields['marque'].required = True
        self.fields['type_materiel'].required = True
        self.fields['type_affectation'].required = True
        self.fields['emplacement'].required = True
        self.fields['etat'].required = True
        self.fields['stock'].required = True
        self.fields['fournisseur'].required = True
        self.fields['date_reception'].required = True
        self.fields['service_affecte'].required = True
        self.fields['utilisateur_affecte'].required = True
        
        # Champs optionnels avec validation
        self.fields['kilometrage'].required = False
        self.fields['defaut_panne'].required = False
        self.fields['reparation'].required = False
        self.fields['reference_piece'].required = False
        self.fields['type_vehicule'].required = False
        self.fields['numero_vehicule'].required = False
        self.fields['date_prochaine_visite'].required = False
        self.fields['prix'].required = False
        
        # Labels personnalisés
        self.fields['kilometrage'].label = "Kilométrage"
        self.fields['defaut_panne'].label = "Défaut/Panne"
        self.fields['reparation'].label = "Réparation"
        self.fields['reference_piece'].label = "Référence pièce"
        self.fields['type_vehicule'].label = "Type véhicule"
        self.fields['numero_vehicule'].label = "Numéro véhicule"
        self.fields['date_prochaine_visite'].label = "Prochaine visite"
        self.fields['prix'].label = "Prix"
        
        # Messages d'aide
        self.fields['kilometrage'].help_text = "Indiquez le kilométrage actuel"
        self.fields['defaut_panne'].help_text = "Type de problème constaté"
        self.fields['reparation'].help_text = "Description des réparations effectuées"
        self.fields['reference_piece'].help_text = "Référence des pièces de rechange"
        self.fields['type_vehicule'].help_text = "Type de véhicule si applicable"
        self.fields['numero_vehicule'].help_text = "Numéro d'immatriculation ou identifiant"
        self.fields['date_prochaine_visite'].help_text = "Date de la prochaine inspection/visite"
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
