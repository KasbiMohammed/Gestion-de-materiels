# Système de Gestion de Matériel

Application web Django pour la gestion complète de matériel avec authentification et gestion des rôles.

## 🚀 Fonctionnalités

### Gestion des Utilisateurs
- **Authentification Django** avec login/logout sécurisé
- **Rôles définis** :
  - **Admin** : Accès complet (CRUD) + Admin Django
  - **User** : Lecture seule (consultation uniquement)
- **Interface adaptative** selon le rôle de l'utilisateur

### Gestion du Matériel
- **CRUD complet** pour les administrateurs
- **Consultation détaillée** pour tous les utilisateurs
- **Recherche avancée** multi-critères
- **Filtrage** par état et type de matériel
- **Pagination** pour les grandes listes

### Caractéristiques du Matériel
- Matricule unique
- Marque et type
- État (Neuf, Bon état, Usé, En panne, Réformé)
- Gestion du stock
- Affectation (service et utilisateur)
- Informations fournisseur et dates
- Observations détaillées

## 🛠️ Technologies

- **Backend** : Django 4.2+ (Python 3.10+)
- **Frontend** : Bootstrap 5 + Font Awesome
- **Base de données** : SQLite (par défaut)
- **Sécurité** : CSRF, authentification Django, permissions

## 📋 Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd gestion_materiel
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer le superutilisateur
```bash
python manage.py createsuperuser
```
Suivez les instructions pour créer un compte administrateur.

### 6. Lancer le serveur
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : http://127.0.0.1:8000

## 👤 Utilisateurs

### Compte Administrateur
- **Accès** : Créé avec `createsuperuser`
- **Permissions** : CRUD complet + Admin Django
- **Interface** : Tous les boutons d'action disponibles

### Compte Utilisateur Standard
- **Création** : Via l'interface Admin Django
- **Permissions** : Lecture seule
- **Interface** : Consultation uniquement

## 📁 Structure du Projet

```
gestion_materiel/
├── manage.py                    # Script de gestion Django
├── requirements.txt             # Dépendances Python
├── README.md                    # Documentation
├── gestion_materiel/            # Projet Django
│   ├── __init__.py
│   ├── settings.py              # Configuration Django
│   ├── urls.py                  # URLs principales
│   ├── wsgi.py                  # WSGI config
│   └── asgi.py                  # ASGI config
├── materiel/                    # App Django
│   ├── __init__.py
│   ├── admin.py                 # Configuration Admin
│   ├── apps.py                  # Configuration App
│   ├── forms.py                 # Formulaires
│   ├── models.py                # Modèles de données
│   ├── urls.py                  # URLs de l'app
│   └── views.py                 # Vues
├── templates/                   # Templates HTML
│   ├── base.html               # Template de base
│   ├── registration/
│   │   └── login.html          # Page de connexion
│   └── materiel/
│       ├── dashboard.html       # Tableau de bord
│       ├── materiel_list.html   # Liste du matériel
│       ├── materiel_detail.html # Détails du matériel
│       ├── materiel_form.html   # Formulaire ajout/modification
│       └── materiel_confirm_delete.html # Confirmation suppression
└── static/                      # Fichiers statiques
    ├── css/
    │   └── style.css           # Styles personnalisés
    └── js/
        └── script.js           # Scripts JavaScript
```

## 🎯 Utilisation

### 1. Connexion
- Accédez à `http://127.0.0.1:8000`
- Connectez-vous avec le compte superutilisateur

### 2. Tableau de bord
- Vue d'ensemble des statistiques
- Liste récente du matériel
- Accès rapide aux fonctionnalités

### 3. Gestion du matériel (Admin)
- **Ajouter** : Cliquez sur "Ajouter du matériel"
- **Modifier** : Bouton "Modifier" sur chaque élément
- **Supprimer** : Bouton "Supprimer" avec confirmation
- **Admin Django** : Menu Administration → Admin Django

### 4. Consultation (User)
- **Liste** : Navigation dans la liste complète
- **Détails** : Cliquez sur le matricule pour voir les détails
- **Recherche** : Utilisez la barre de recherche
- **Filtres** : Filtrez par état et type

## 🔧 Configuration

### Base de données PostgreSQL (optionnel)
Modifiez `gestion_materiel/settings.py` :
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestion_materiel',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Installez le driver PostgreSQL :
```bash
pip install psycopg2-binary
```

### Personnalisation
- **Styles** : Modifiez `static/css/style.css`
- **Templates** : Personnalisez les fichiers HTML
- **Modèles** : Étendez `materiel/models.py`
- **Permissions** : Ajoutez des rôles personnalisés

## 📊 Fonctionnalités Avancées

### Recherche et Filtrage
- Recherche textuelle sur plusieurs champs
- Filtres par état et type de matériel
- Pagination pour gérer les grands volumes

### Interface Responsive
- Adaptation mobile/tablette
- Design moderne avec Bootstrap 5
- Animations et transitions fluides

### Sécurité
- Protection CSRF
- Authentification sécurisée
- Permissions par rôle
- Validation des formulaires

## 🤝 Contribuer

1. Fork le projet
2. Créer une branche de fonctionnalité
3. Commit les changements
4. Push vers la branche
5. Créer une Pull Request

## 📝 Licence

Ce projet est sous licence MIT.

## 🆘 Support

Pour toute question ou problème :
- Vérifiez la documentation
- Consultez les logs Django
- Testez avec différents navigateurs

---

**Développé avec Django 4.2+ • Python 3.10+**
"# Gestion-de-mat�riels"  
"# Gestion-de-materiels" 
"# Gestion-de-mat�riels" 
