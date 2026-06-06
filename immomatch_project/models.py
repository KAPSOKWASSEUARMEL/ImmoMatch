from django.db import models
from django.contrib.auth.models import User

class House(models.Model):
    # Available options for the property type
    PROPERTY_TYPE_CHOICES = [
        ('ROOM', 'Room'),
        ('STUDIO', 'Studio'),
        ('APARTMENT', 'Apartment'),
        ('VILLA', 'Villa'),
    ]

    # Secure relationship link to Django's built-in User model
    # If a user account is deleted, their listings are also deleted (models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='houses')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # DecimalField is ideal for financial data to avoid floating-point rounding errors
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='STUDIO')
    
    # Amenities (Boolean fields: True or False)
    has_borehole = models.BooleanField(default=False, verbose_name="Borehole / Water available")
    has_parking = models.BooleanField(default=False, verbose_name="Parking space available")
    
    main_image = models.ImageField(upload_to='houses/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.property_type} - {self.city} ({self.price} CFA)"
    

    from django.db import models
from django.contrib.auth.models import User

# Nouveau modèle de sécurité pour traquer les connexions
class ConnexionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur traqué")
    ip_address = models.GenericIPAddressField(verbose_name="Adresse IP")
    user_agent = models.TextField(verbose_name="Navigateur / Appareil")
    date_connexion = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de connexion")

    class Meta:
        verbose_name = "Log de Sécurité"
        verbose_name_plural = "Logs de Sécurité"
        ordering = ['-date_connexion'] # Affiche les connexions les plus récentes en premier

    def __str__(self):
        return f"{self.user.username} connecté depuis l'IP {self.ip_address} le {self.date_connexion}"