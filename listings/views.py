import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import House

# =========================================================================
# 1. CONFIGURATION DU TRAQUEUR DE SÉCURITÉ (Fichier journal externe)
# =========================================================================
logger = logging.getLogger('security_tracker')
logging.basicConfig(
    filename='security_audit.log',
    level=logging.INFO,
    format='%(asctime)s | ALERT_SECURITY | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# =========================================================================
# 2. DICTIONNAIRE GLOBAL DE TRADUCTION (Contournement du blocage Windows)
# =========================================================================
TRANSLATIONS = {
    'en': {
        # Textes de la page d'accueil (Liste)
        'list_title': "House Listings",
        'welcome': "Welcome",
        'logout': "Log out",
        'login': "Log in",
        'register': "Register",
        'main_welcome': "Welcome to ImmoMatch",
        'subtitle': "Find your ideal rental property safely.",
        'filter_title': "Filter available accommodations",
        'label_city': "City :",
        'label_neighborhood': "Neighborhood :",
        'label_budget': "Max budget (FCFA) :",
        'btn_search': "Search",
        'btn_clear': "Clear",
        'section_title': "Available houses",
        'no_image': "No image available",
        'btn_details': "View Details",
        'no_results': "No accommodation matches your exact search criteria.",
        
        # Textes de la page de détails
        'detail_title': "Property Details",
        'back_list': "⬅️ Back to listings",
        'description_title': "Description",
        'contact_landlord': "📞 Contact Landlord",
        'whatsapp_btn': "Chat on WhatsApp",
        'security_notice': "🔒 Security Check",
        'anon_warning': "You must be logged in to view the landlord's WhatsApp contact. This measure prevents fraud and protects our community.",
        'price_per_month': "FCFA / month"
    },
    'fr': {
        # Textes de la page d'accueil (Liste)
        'list_title': "Liste des Maisons",
        'welcome': "Bienvenue",
        'logout': "Se déconnecter",
        'login': "Se connecter",
        'register': "S'inscrire",
        'main_welcome': "Bienvenue sur ImmoMatch",
        'subtitle': "Trouvez votre bien locatif idéal en toute sécurité.",
        'filter_title': "Filtrer les logements disponibles",
        'label_city': "Ville :",
        'label_neighborhood': "Quartier :",
        'label_budget': "Budget max (FCFA) :",
        'btn_search': "Rechercher",
        'btn_clear': "Effacer",
        'section_title': "Maisons disponibles",
        'no_image': "Aucune image disponible",
        'btn_details': "Voir les détails",
        'no_results': "Aucun logement ne correspond exactement à vos critères de recherche.",
        
        # Textes de la page de détails
        'detail_title': "Détails du Logement",
        'back_list': "⬅️ Retour à la liste",
        'description_title': "Description du bien",
        'contact_landlord': "📞 Contacter le Bailleur",
        'whatsapp_btn': "Discuter sur WhatsApp",
        'security_notice': "🔒 Contrôle de Sécurité",
        'anon_warning': "Vous devez être connecté pour voir le contact WhatsApp du bailleur. Cette mesure évite les fraudes et protège notre communauté.",
        'price_per_month': "FCFA / mois"
    }
}

# =========================================================================
# 3. LES VUES (FONCTIONS LOGIQUES DE L'APPLICATION)
# =========================================================================

def house_list(request):
    """Affiche la liste des maisons et gère le basculement de langue (Français/Anglais)."""
    houses = House.objects.all()
    
    # Gestion de la langue active
    lang = request.GET.get('lang', request.session.get('django_language', 'fr'))
    if lang not in ['fr', 'en']:
        lang = 'fr'
    request.session['django_language'] = lang 
    
    text = TRANSLATIONS[lang]
    
    # Moteur de recherche et filtrage dynamique
    city_query = request.GET.get('city', '').strip()
    neighborhood_query = request.GET.get('neighborhood', '').strip()
    price_max_query = request.GET.get('price_max', '').strip()
    
    if city_query:
        houses = houses.filter(city__icontains=city_query)
    if neighborhood_query:
        houses = houses.filter(neighborhood__icontains=neighborhood_query)
    if price_max_query:
        try:
            houses = houses.filter(price__lte=float(price_max_query))
        except ValueError:
            pass

    context = {
        'houses': houses,
        'city_query': city_query,
        'neighborhood_query': neighborhood_query,
        'price_max_query': price_max_query,
        'text': text, 
        'current_lang': lang,
    }
    return render(request, 'listings/house_list.html', context)


def house_detail(request, pk):
    """Affiche les détails et traque l'identité de l'utilisateur connecté."""
    house = get_object_or_404(House, pk=pk)
    
    # Gestion de la langue active pour les détails
    lang = request.session.get('django_language', 'fr')
    text = TRANSLATIONS[lang]
    
    # Traquage de sécurité si l'utilisateur est connecté
    if request.user.is_authenticated:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        user_agent = request.META.get('HTTP_USER_AGENT', 'Inconnu')
        
        logger.info(
            f"Utilisateur: {request.user.username} (ID: {request.user.id}) | "
            f"IP: {ip} | "
            f"A consulté le contact WhatsApp du bailleur pour le logement ID: {house.id} ({house.title}) | "
            f"Navigateur: {user_agent}"
        )

    context = {
        'house': house,
        'text': text,
        'current_lang': lang,
    }
    return render(request, 'listings/house_detail.html', context)


def register(request):
    """Gère l'inscription sécurisée des nouveaux locataires."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé avec succès pour {username} !')
            return redirect('listings:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'listings/register.html', {'form': form})