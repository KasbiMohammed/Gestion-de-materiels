from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('materiel/', views.MaterielListView.as_view(), name='materiel_list'),
    path('materiel/<int:pk>/', views.MaterielDetailView.as_view(), name='materiel_detail'),
    path('materiel/ajouter/', views.MaterielCreateView.as_view(), name='materiel_create'),
    path('materiel/<int:pk>/modifier/', views.MaterielUpdateView.as_view(), name='materiel_update'),
    path('materiel/<int:pk>/supprimer/', views.MaterielDeleteView.as_view(), name='materiel_delete'),
    path('suivi-visites/', views.VisiteCreateSimpleView.as_view(), name='suivi_visites'),
    path('visite/<int:pk>/', views.VisiteDetailView.as_view(), name='visite_detail'),
    path('visite/<int:pk>/modifier/', views.VisiteUpdateView.as_view(), name='visite_update'),
    path('visite/<int:pk>/supprimer/', views.VisiteDeleteView.as_view(), name='visite_delete'),
]
