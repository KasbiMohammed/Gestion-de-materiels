from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Count, Case, When, Value, IntegerField, Q
from django.utils import timezone
from datetime import timedelta
from .models import Materiel, Visite, ControleVisite
from .forms import MaterielForm, VisiteForm, ControleVisiteForm


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect('dashboard')


class DashboardView(LoginRequiredMixin, ListView):
    model = Materiel
    template_name = 'materiel/dashboard.html'
    context_object_name = 'materiels'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_materiels'] = Materiel.objects.count()
        context['en_stock'] = Materiel.objects.filter(stock__gt=0).count()
        context['en_panne'] = Materiel.objects.filter(etat='panne').count()
        context['reforme'] = Materiel.objects.filter(etat='reforme').count()
        context['is_staff'] = self.request.user.is_staff
        return context

    def get_queryset(self):
        queryset = Materiel.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(matricule__icontains=search) |
                Q(marque__icontains=search) |
                Q(type_materiel__icontains=search) |
                Q(service_affecte__icontains=search) |
                Q(utilisateur_affecte__icontains=search)
            )
        return queryset


class MaterielListView(LoginRequiredMixin, ListView):
    model = Materiel
    template_name = 'materiel/materiel_list.html'
    context_object_name = 'materiels'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = self.request.user.is_staff
        
        # Ajouter le formulaire de visite rapide
        context['visite_form'] = VisiteForm()
        
        return context

    def get_queryset(self):
        queryset = Materiel.objects.all()
        search = self.request.GET.get('search')
        etat_filter = self.request.GET.get('etat')
        type_filter = self.request.GET.get('type_materiel')
        show_all = self.request.GET.get('all')
        
        if search:
            queryset = queryset.filter(
                Q(matricule__icontains=search) |
                Q(marque__icontains=search) |
                Q(type_materiel__icontains=search) |
                Q(service_affecte__icontains=search) |
                Q(utilisateur_affecte__icontains=search)
            )
        
        if etat_filter:
            queryset = queryset.filter(etat=etat_filter)
        
        if type_filter:
            queryset = queryset.filter(type_materiel=type_filter)
        
        return queryset
    
    def get_paginate_by(self, queryset):
        # Si le paramètre 'all' est présent, ne pas paginer
        if self.request.GET.get('all'):
            return None
        return 20


class MaterielDetailView(LoginRequiredMixin, DetailView):
    model = Materiel
    template_name = 'materiel/materiel_detail.html'
    context_object_name = 'materiel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = self.request.user.is_staff
        context['visites'] = self.object.visites.all().order_by('-date_visite')
        return context


class MaterielCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Materiel
    form_class = MaterielForm
    template_name = 'materiel/materiel_form.html'
    success_url = reverse_lazy('materiel_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter le formulaire de visite existant
        context['visite_form'] = VisiteForm()
        context['show_visite_form'] = True  # Indicateur pour le template
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Créer automatiquement une visite liée pour TOUS les matériels (pas seulement les véhicules)
        type_visite = form.cleaned_data.get('type_visite', 'entretien')
        
        # Récupérer les champs de maintenance du formulaire
        prix = form.cleaned_data.get('prix', 0)
        
        # Créer la visite liée avec seulement les champs existants dans le modèle
        visite = Visite.objects.create(
            materiel=self.object,
            date_visite=timezone.now().date(),
            type_visite=type_visite,
            observations=f'Visite initiale ({type_visite}) - Création automatique lors de l\'ajout du matériel',
            responsable='Système',
            cout=prix
        )
        
        # Message de succès
        messages.success(self.request, f'Matériel ajouté avec succès! Une visite de type "{type_visite}" a été créée automatiquement.')
        
        # Rediriger vers la page de suivi des visites pour voir l'historique mis à jour
        return redirect('suivi_visites')


class MaterielUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Materiel
    form_class = MaterielForm
    template_name = 'materiel/materiel_form.html'
    success_url = reverse_lazy('materiel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Matériel mis à jour avec succès!')
        return super().form_valid(form)


class MaterielDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Materiel
    template_name = 'materiel/materiel_confirm_delete.html'
    success_url = reverse_lazy('materiel_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Matériel supprimé avec succès!')
        return super().delete(request, *args, **kwargs)


class SuiviVisitesView(LoginRequiredMixin, ListView):
    model = Materiel
    template_name = 'materiel/suivi_visites.html'  # Template existant
    context_object_name = 'vehicules'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ajouter les formulaires existants
        context['materiel_form'] = MaterielForm()
        context['visite_form'] = VisiteForm()
        
        # Filtres
        vehicule_filter = self.request.GET.get('vehicule')
        matricule_filter = self.request.GET.get('matricule')
        date_filter = self.request.GET.get('date')
        type_visite_filter = self.request.GET.get('type_visite')
        sort_order = self.request.GET.get('sort', 'date_desc')
        
        # Récupérer tous les véhicules
        vehicules = Materiel.objects.filter(type_materiel='vehicule')
        
        # Appliquer le filtre par matricule si spécifié
        if matricule_filter:
            vehicules = vehicules.filter(matricule__icontains=matricule_filter)
        
        # Appliquer le filtre véhicule si spécifié
        if vehicule_filter:
            vehicules = vehicules.filter(id=vehicule_filter)
        
        # Récupérer toutes les visites avec filtres
        visites_queryset = Visite.objects.all()
        
        if matricule_filter:
            visites_queryset = visites_queryset.filter(materiel__matricule__icontains=matricule_filter)
        
        if vehicule_filter:
            visites_queryset = visites_queryset.filter(materiel_id=vehicule_filter)
        
        if date_filter:
            visites_queryset = visites_queryset.filter(date_visite=date_filter)
        
        if type_visite_filter:
            visites_queryset = visites_queryset.filter(type_visite=type_visite_filter)
        
        # Trier les visites
        if sort_order == 'date_asc':
            visites_queryset = visites_queryset.order_by('date_visite')
        else:
            visites_queryset = visites_queryset.order_by('-date_visite')
        
        # Préparer la liste des véhicules pour la recherche JavaScript
        vehicules_list = list(vehicules.values('id', 'matricule', 'marque', 'type_materiel'))
        
        # Calculer les statistiques
        total_visites = visites_queryset.count()
        visites_ce_mois = visites_queryset.filter(
            date_visite__month=timezone.now().month,
            date_visite__year=timezone.now().year
        ).count()
        
        # Visites planifiées à venir
        visites_avenir = Visite.objects.filter(
            date_visite__gt=timezone.now().date()
        ).order_by('date_visite')[:5]
        
        # Véhicules avec visites bientôt dues
        alertes_visites = []
        aujourdhui = timezone.now().date()
        for vehicule in vehicules:  # Utiliser la liste déjà filtrée
            derniere_visite = vehicule.visites.first()
            if derniere_visite and derniere_visite.prochaine_visite:
                jours_restants = (derniere_visite.prochaine_visite - aujourdhui).days
                if jours_restants <= 30 and jours_restants >= 0:
                    alertes_visites.append({
                        'vehicule': vehicule,
                        'jours_restants': jours_restants,
                        'prochaine_visite': derniere_visite.prochaine_visite
                    })
        
        context.update({
            'vehicules': vehicules,
            'total_visites': total_visites,
            'visites_ce_mois': visites_ce_mois,
            'visites_avenir': visites_avenir,
            'alertes_visites': alertes_visites,
            'type_visite_choices': Visite.TYPE_VISITE_CHOICES,
            'vehicule_filter': vehicule_filter,
            'matricule_filter': matricule_filter,
            'date_filter': date_filter,
            'type_visite_filter': type_visite_filter,
            'sort_order': sort_order,
            'vehicules_list': vehicules_list,
            'is_staff': self.request.user.is_staff,
        })
        
        return context

    def get_queryset(self):
        return Materiel.objects.filter(type_materiel='vehicule')


class VisiteCreateSimpleView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'materiel/suivi_visites.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ajouter les formulaires existants
        context['materiel_form'] = MaterielForm()
        context['visite_form'] = VisiteForm()
        
        # Filtres
        vehicule_filter = self.request.GET.get('vehicule')
        matricule_filter = self.request.GET.get('matricule')
        date_filter = self.request.GET.get('date')
        type_visite_filter = self.request.GET.get('type_visite')
        sort_order = self.request.GET.get('sort', 'date_desc')
        
        # Récupérer tous les véhicules
        vehicules = Materiel.objects.filter(type_materiel='vehicule')
        
        # Appliquer le filtre par matricule si spécifié
        if matricule_filter:
            vehicules = vehicules.filter(matricule__icontains=matricule_filter)
        
        # Appliquer le filtre véhicule si spécifié
        if vehicule_filter:
            vehicules = vehicules.filter(id=vehicule_filter)
        
        # Récupérer toutes les visites avec filtres
        visites_queryset = Visite.objects.all()
        
        if matricule_filter:
            visites_queryset = visites_queryset.filter(materiel__matricule__icontains=matricule_filter)
        
        if vehicule_filter:
            visites_queryset = visites_queryset.filter(materiel_id=vehicule_filter)
        
        if date_filter:
            visites_queryset = visites_queryset.filter(date_visite=date_filter)
        
        if type_visite_filter:
            visites_queryset = visites_queryset.filter(type_visite=type_visite_filter)
        
        # Trier les visites
        if sort_order == 'date_asc':
            visites_queryset = visites_queryset.order_by('date_visite')
        else:
            visites_queryset = visites_queryset.order_by('-date_visite')
        
        # Préparer la liste des véhicules pour la recherche JavaScript
        vehicules_list = list(vehicules.values('id', 'matricule', 'marque', 'type_materiel'))
        
        # Calculer les statistiques
        total_visites = visites_queryset.count()
        visites_ce_mois = visites_queryset.filter(
            date_visite__month=timezone.now().month,
            date_visite__year=timezone.now().year
        ).count()
        
        # Visites planifiées à venir
        visites_avenir = Visite.objects.filter(
            date_visite__gt=timezone.now().date()
        ).order_by('date_visite')[:5]
        
        # Véhicules avec visites bientôt dues
        alertes_visites = []
        aujourdhui = timezone.now().date()
        for vehicule in vehicules:  # Utiliser la liste déjà filtrée
            derniere_visite = vehicule.visites.first()
            if derniere_visite and derniere_visite.prochaine_visite:
                jours_restants = (derniere_visite.prochaine_visite - aujourdhui).days
                if jours_restants <= 30 and jours_restants >= 0:
                    alertes_visites.append({
                        'vehicule': vehicule,
                        'jours_restants': jours_restants,
                        'prochaine_visite': derniere_visite.prochaine_visite
                    })
        
        context.update({
            'vehicules': vehicules,
            'total_visites': total_visites,
            'visites_ce_mois': visites_ce_mois,
            'visites_avenir': visites_avenir,
            'alertes_visites': alertes_visites,
            'type_visite_choices': Visite.TYPE_VISITE_CHOICES,
            'vehicule_filter': vehicule_filter,
            'matricule_filter': matricule_filter,
            'date_filter': date_filter,
            'type_visite_filter': type_visite_filter,
            'sort_order': sort_order,
            'vehicules_list': vehicules_list,
            'is_staff': self.request.user.is_staff,
        })
        
        return context
    
    def post(self, request, *args, **kwargs):
        materiel_id = request.POST.get('materiel_id')
        date_visite = request.POST.get('date_visite')
        type_visite = request.POST.get('type_visite')
        responsable = request.POST.get('responsable', '')
        kilometrage = request.POST.get('kilometrage')
        cout = request.POST.get('cout')
        prochaine_visite = request.POST.get('prochaine_visite')
        observations = request.POST.get('observations', '')
        
        if not materiel_id or not date_visite or not type_visite:
            messages.error(request, 'Les champs Matériel, Date de visite et Type de visite sont obligatoires.')
            # Rediriger vers la même page pour afficher les erreurs
            return self.get(request)
        
        try:
            materiel = Materiel.objects.get(id=materiel_id)
            
            # Créer la visite
            visite = Visite.objects.create(
                materiel=materiel,
                date_visite=date_visite,
                type_visite=type_visite,
                responsable=responsable,
                kilometrage=kilometrage if kilometrage else None,
                cout=cout if cout else None,
                prochaine_visite=prochaine_visite if prochaine_visite else None,
                observations=observations
            )
            
            messages.success(request, f'Visite ajoutée avec succès pour {materiel.matricule}!')
            # Rediriger vers la même page pour voir l'historique mis à jour
            return self.get(request)
            
        except Materiel.DoesNotExist:
            messages.error(request, 'Matériel non trouvé. Veuillez sélectionner un matériel valide.')
            return self.get(request)
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout de la visite: {str(e)}')
            return self.get(request)


class VisiteAjoutRapideView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'materiel/visite_ajout_rapide.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_visite_choices'] = Visite.TYPE_VISITE_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        materiel_id = request.POST.get('materiel_id')
        date_visite = request.POST.get('date_visite')
        type_visite = request.POST.get('type_visite')
        responsable = request.POST.get('responsable', '')
        kilometrage = request.POST.get('kilometrage')
        cout = request.POST.get('cout')
        prochaine_visite = request.POST.get('prochaine_visite')
        observations = request.POST.get('observations', '')
        
        if not materiel_id or not date_visite or not type_visite:
            messages.error(request, 'Les champs Matériel, Date de visite et Type de visite sont obligatoires.')
            return redirect('visite_ajout_rapide')
        
        try:
            materiel = Materiel.objects.get(id=materiel_id)
            
            # Créer la visite
            visite = Visite.objects.create(
                materiel=materiel,
                date_visite=date_visite,
                type_visite=type_visite,
                responsable=responsable,
                kilometrage=kilometrage if kilometrage else None,
                cout=cout if cout else None,
                prochaine_visite=prochaine_visite if prochaine_visite else None,
                observations=observations
            )
            
            messages.success(request, f'Visite ajoutée avec succès pour {materiel.matricule}!')
            return redirect('suivi_visites')
            
        except Materiel.DoesNotExist:
            messages.error(request, 'Matériel non trouvé. Veuillez sélectionner un matériel valide.')
            return redirect('visite_ajout_rapide')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout de la visite: {str(e)}')
            return redirect('visite_ajout_rapide')


class VisiteCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Visite
    form_class = VisiteForm
    template_name = 'materiel/visite_form.html'
    success_url = reverse_lazy('suivi_visites')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ajouter une visite'
        
        # Pré-remplir le matériel si passé en paramètre
        materiel_id = self.request.GET.get('materiel')
        if materiel_id:
            try:
                materiel = Materiel.objects.get(id=materiel_id)
                context['materiel_preselectionne'] = materiel
                # Pré-remplir le formulaire avec le matériel
                if 'form' not in context:
                    context['form'] = self.get_form()
                context['form'].initial['materiel'] = materiel
            except Materiel.DoesNotExist:
                pass
        
        context['is_staff'] = self.request.user.is_staff
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Visite ajoutée avec succès pour {form.instance.materiel.matricule}!')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Rediriger vers la page de suivi des visites ou vers le détail du matériel
        if self.object.materiel:
            return reverse_lazy('materiel_detail', kwargs={'pk': self.object.materiel.pk})
        return reverse_lazy('suivi_visites')


class VisiteDetailView(LoginRequiredMixin, DetailView):
    model = Visite
    template_name = 'materiel/visite_detail.html'
    context_object_name = 'visite'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = self.request.user.is_staff
        context['controles'] = self.object.controles.all()
        context['visites'] = self.object.materiel.visites.all().order_by('-date_visite')
        return context


class VisiteUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Visite
    form_class = VisiteForm
    template_name = 'materiel/visite_form.html'
    success_url = reverse_lazy('suivi_visites')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Modifier la visite - {self.object.materiel.matricule}'
        return context


class VisiteDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Visite
    template_name = 'materiel/visite_confirm_delete.html'
    success_url = reverse_lazy('suivi_visites')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Supprimer la visite - {self.object.materiel.matricule}'
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Visite du {self.object.materiel.matricule} supprimée avec succès.')
        return super().delete(request, *args, **kwargs)
