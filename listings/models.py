from django.db import models
from django.contrib.auth.models import User

class House(models.Model):
    PROPERTY_TYPES = [
        ('studio', 'Studio'),
        ('apartment', 'Appartement'),
        ('house', 'Maison Complète'),
        ('room', 'Chambre'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    city = models.CharField(max_length=100)          
    neighborhood = models.CharField(max_length=100)  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    
    # Image principale corrigée (upload_to)
    main_image = models.ImageField(upload_to='houses/main/', blank=True, null=True)
    
    agent_phone = models.CharField(max_length=20)    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.city} ({self.price} FCFA)"


class HouseImage(models.Model):
    """Modèle permettant d'associer un catalogue de plusieurs photos à une seule maison."""
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='images')
    # Image secondaire corrigée (upload_to)
    image = models.ImageField(upload_to='houses/catalog/')
    caption = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return f"Photo pour : {self.house.title}"