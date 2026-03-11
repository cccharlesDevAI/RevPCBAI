import firebase_admin
from firebase_admin import credentials, db
import os
import time

# --- Configuration Firebase ---
# IMPORTANT : Remplace '''path/to/your/serviceAccountKey.json''' par le chemin
# vers ton propre fichier de clé de service Firebase.
cred = credentials.Certificate('''path/to/your/serviceAccountKey.json''')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://revpcbai-default-rtdb.firebaseio.com'
})

def handle_command(event):
    """Callback qui se déclenche quand la donnée 'commande' change."""
    print(f"Événement reçu : {event.path}, {event.data}")
    if event.path == "/" and event.data and event.data.get("action") == "LANCER_ROUTAGE":
        print("💎 [IA] Commande de routage reçue de Firebase !")
        print("✍️ [ACTION] Début de l'injection des pistes dans KiCad...")

        # ICI : Ton script qui fait bouger la souris pour dessiner le PCB
        # Assure-toi que python3 est dans ton PATH sur le Pi
        os.system("python3 usb_injector.py")

        # Optionnel : Remettre à zéro la commande pour ne pas la relancer
        db.reference('commande').set({})
        print("✅ [IA] Opération terminée. En attente de la prochaine commande.")

def monitor_firebase_orders():
    print("🚀 STATION REVPCBAI ACTIVE - PRÊTE POUR LE ROUTAGE (via Firebase)")
    # Écoute les changements sur le nœud 'commande'
    db.reference('commande').listen(handle_command)

if __name__ == "__main__":
    monitor_firebase_orders()
    # Boucle infinie pour garder le script en vie
    while True:
        time.sleep(1)
