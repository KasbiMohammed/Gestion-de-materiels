from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Case, When, Value, IntegerField
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
        return context

    def get_queryset(self):
        queryset = Materiel.objects.all()
        search = self.request.GET.get('search')
        etat_filter = self.request.GET.get('etat')
        type_filter = self.request.GET.get('type_materiel')
        
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

    def form_valid(self, form):
        messages.success(self.request, 'Matériel ajouté avec succès!')
        return super().form_valid(form)


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
    template_name = 'materiel/suivi_visites.html'
    context_object_name = 'vehicules'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtres
        vehicule_filter = self.request.GET.get('vehicule')
        date_filter = self.request.GET.get('date')
        type_visite_filter = self.request.GET.get('type_visite')
        sort_order = self.request.GET.get('sort', 'date_desc')
        
        # Récupérer tous les véhicules
        vehicules = Materiel.objects.filter(type_materiel='vehicule')
        
        # Appliquer le filtre véhicule si spécifié
        if vehicule_filter:
            vehicules = vehicules.filter(id=vehicule_filter)
        
        # Récupérer toutes les visites avec filtres
        visites_queryset = Visite.objects.all()
        
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
        
        # Organiser les visites par véhicule - utilisation des relations Django
        # Les visites seront accessibles directement via vehicule.visites.all dans le template
        
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
        for vehicule in Materiel.objects.filter(type_materiel='vehicule'):
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
            'vehicules_list': vehicules,
            'total_visites': total_visites,
            'visites_ce_mois': visites_ce_mois,
            'visites_avenir': visites_avenir,
            'alertes_visites': alertes_visites,
            'type_visite_choices': Visite.TYPE_VISITE_CHOICES,
            'vehicule_filter': vehicule_filter,
            'date_filter': date_filter,
            'type_visite_filter': type_visite_filter,
            'sort_order': sort_order,
            'is_staff': self.request.user.is_staff,
        })
        
        return context

    def get_queryset(self):
        return Materiel.objects.filter(type_materiel='vehicule')


class VisiteCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Visite
    form_class = VisiteForm
    template_name = 'materiel/visite_form.html'
    success_url = reverse_lazy('suivi_visites')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ajouter une visite"
        context['is_staff'] = self.request.user.is_staff
        
        # Pré-sélectionner le véhicule si passé en paramètre
        materiel_id = self.request.GET.get('materiel')
        if materiel_id:
            try:
                materiel = Materiel.objects.get(id=materiel_id, type_materiel='vehicule')
                context['selected_materiel'] = materiel
            except Materiel.DoesNotExist:
                pass
        
        return context

    def get_initial(self):
        initial = super().get_initial()
        materiel_id = self.request.GET.get('materiel')
        if materiel_id:
            initial['materiel'] = materiel_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Visite ajoutée avec succès!')
        return super().form_valid(form)


class VisiteDetailView(LoginRequiredMixin, DetailView):
    model = Visite
    template_name = 'materiel/visite_detail.html'
    context_object_name = 'visite'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = self.request.user.is_staff
        context['controles'] = self.object.controles.all()
        return context
