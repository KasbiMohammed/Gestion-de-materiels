// Scripts JavaScript pour l'application de gestion de matériel

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des composants
    initializeTooltips();
    initializeConfirmations();
    initializeSearch();
    initializeAutoComplete();
});

// Initialisation des tooltips Bootstrap
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialisation des confirmations pour les actions destructives
function initializeConfirmations() {
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

// Initialisation de la recherche en temps réel
function initializeSearch() {
    const searchInput = document.getElementById('search');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const value = this.value;
            
            // Attendre 300ms après la fin de la saisie
            searchTimeout = setTimeout(function() {
                if (value.length > 2 || value.length === 0) {
                    // Soumettre le formulaire de recherche
                    const form = searchInput.closest('form');
                    if (form) {
                        form.submit();
                    }
                }
            }, 300);
        });
    }
}

// Initialisation de l'auto-complétion pour certains champs
function initializeAutoComplete() {
    // Auto-complétion pour le champ matricule (formatage automatique)
    const matriculeField = document.getElementById('id_matricule');
    if (matriculeField) {
        matriculeField.addEventListener('input', function() {
            // Mettre en majuscules automatiquement
            this.value = this.value.toUpperCase();
        });
    }
    
    // Auto-complétion pour le champ service (suggestions basées sur les services existants)
    const serviceField = document.getElementById('id_service_affecte');
    if (serviceField) {
        // Liste des services courants
        const services = [
            'Direction Générale',
            'Ressources Humaines',
            'Finance',
            'Informatique',
            'Marketing',
            'Production',
            'Logistique',
            'Maintenance',
            'Qualité',
            'Achat',
            'Commercial',
            'Juridique'
        ];
        
        // Créer un datalist pour les suggestions
        const datalist = document.createElement('datalist');
        datalist.id = 'services-suggestions';
        services.forEach(service => {
            const option = document.createElement('option');
            option.value = service;
            datalist.appendChild(option);
        });
        
        serviceField.setAttribute('list', 'services-suggestions');
        serviceField.parentNode.appendChild(datalist);
    }
}

// Fonction pour afficher des notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-suppression après 5 secondes
    setTimeout(function() {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Fonction pour valider le formulaire avant soumission
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Fonction pour formater les nombres
function formatNumber(number) {
    return new Intl.NumberFormat('fr-FR').format(number);
}

// Fonction pour formater les dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Fonction pour exporter les données en CSV
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        
        cols.forEach(col => {
            // Supprimer les balises HTML et nettoyer le texte
            let text = col.textContent.trim();
            text = text.replace(/"/g, '""'); // Échapper les guillemets
            if (text.includes(',') || text.includes('"') || text.includes('\n')) {
                text = `"${text}"`; // Encadrer avec des guillemets si nécessaire
            }
            rowData.push(text);
        });
        
        csv.push(rowData.join(','));
    });
    
    // Créer et télécharger le fichier CSV
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename || 'export.csv');
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Fonction pour imprimer une section
function printSection(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Impression</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { padding: 20px; }
                .no-print { display: none !important; }
                @media print {
                    body { padding: 0; }
                }
            </style>
        </head>
        <body>
            ${element.innerHTML}
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

// Gestion des messages flash
function initializeMessages() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Initialisation des messages au chargement
initializeMessages();
