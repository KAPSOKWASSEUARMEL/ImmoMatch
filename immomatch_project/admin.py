from django.contrib import admin
from .models import House, HouseImage

class HouseImageInline(admin.StackedInline):
    """Permet d'ajouter des photos au catalogue directement depuis la fiche de la maison."""
    model = HouseImage
    extra = 3  # Affiche par défaut 3 emplacements vides pour charger des photos secondaires

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    # Liste des champs réels existants à afficher dans le tableau de l'administration
    list_display = ('title', 'city', 'neighborhood', 'price', 'property_type', 'created_at')
    
    # Filtres latéraux basés uniquement sur les champs existants
    list_filter = ('city', 'property_type')
    
    # Barre de recherche pour retrouver rapidement un logement
    search_fields = ('title', 'city', 'neighborhood', 'description')
    
    # Intégration du catalogue multi-photos sur la même page
    inlines = [HouseImageInline]