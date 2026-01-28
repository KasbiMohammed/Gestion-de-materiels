from django import forms
from .models import Materiel


class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = [
            'date', 'matricule', 'marque', 'type_materiel', 'type_affectation',
            'emplacement', 'etat', 'stock', 'fournisseur', 'date_reception',
            'observation', 'service_affecte', 'utilisateur_affecte'
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
            'observation': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'service_affecte': forms.TextInput(attrs={'class': 'form-control'}),
            'utilisateur_affecte': forms.TextInput(attrs={'class': 'form-control'}),
        }
