from django.contrib import admin
from .models import Materiel


@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = [
        'matricule', 'marque', 'type_materiel', 'etat', 
        'stock', 'service_affecte', 'utilisateur_affecte', 
        'date_reception', 'created_at'
    ]
    list_filter = [
        'type_materiel', 'type_affectation', 'etat', 
        'service_affecte', 'date_reception'
    ]
    search_fields = [
        'matricule', 'marque', 'fournisseur', 
        'service_affecte', 'utilisateur_affecte'
    ]
    list_editable = ['etat', 'stock']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('date', 'matricule', 'marque', 'type_materiel', 'type_affectation')
        }),
        ('État et emplacement', {
            'fields': ('emplacement', 'etat', 'stock')
        }),
        ('Fournisseur et réception', {
            'fields': ('fournisseur', 'date_reception')
        }),
        ('Affectation', {
            'fields': ('service_affecte', 'utilisateur_affecte')
        }),
        ('Observations', {
            'fields': ('observation',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
