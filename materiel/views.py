from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Materiel
from .forms import MaterielForm


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
