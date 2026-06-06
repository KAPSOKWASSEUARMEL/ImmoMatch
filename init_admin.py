import os
import django

# 1. Indique à Python quel fichier de configuration utiliser
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immomatch_project.settings')

# 2. Initialise le framework Django
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    
    # Récupère les valeurs depuis les variables d'environnement (locales ou en ligne)
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@immomatch.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'ImmoMatch2026!')

    # Vérifie si cet administrateur existe déjà pour éviter les doublons et les plantages
    if not User.objects.filter(username=username).exists():
        print(f"Création automatique du superutilisateur : {username}...")
        try:
            # Exécute la commande native de Django de manière automatique
            call_command(
                'createsuperuser',
                interactive=False,
                username=username,
                email=email
            )
            # Applique manuellement le mot de passe de manière sécurisée
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            print("Superutilisateur créé avec succès !")
        except Exception as e:
            print(f"Erreur lors de la création : {e}")
    else:
        print(f"L'utilisateur '{username}' existe déjà en base de données.")

if __name__ == '__main__':
    create_admin()