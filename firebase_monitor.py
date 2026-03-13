import firebase_admin
from firebase_admin import credentials, db
import os
import time
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# 🔥 INITIALISATION FIREBASE
# ==========================================
FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH", "firebase-service-account.json")
FIREBASE_URL = os.getenv("FIREBASE_URL")

if not FIREBASE_URL:
    raise EnvironmentError("❌ FIREBASE_URL manquante dans le fichier .env")

if not os.path.exists(FIREBASE_CRED_PATH):
    raise FileNotFoundError(f"❌ Fichier credentials introuvable : {FIREBASE_CRED_PATH}")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_URL
    })


def handle_command(event):
    """Callback qui se déclenche quand un nœud /revpcbai_commands change."""
    print(f"Événement reçu : {event.path}, {event.data}")
    data = event.data

    # Format daemon : {type, action, timestamp, status}
    if isinstance(data, dict):
        action = data.get("action") or data.get("type", "")
        if action in ("LANCER_ROUTAGE", "LANCER_INJECTION", "scan_and_clone_pcb"):
            print("💎 [IA] Commande reçue depuis Firebase !")
            print("✍️  [ACTION] Début de l'injection des pistes dans KiCad...")

            os.system("python3 usb_injector.py")

            # Marquer comme traité
            db.reference(f'revpcbai_commands{event.path}').update({'status': 'processed'})
            print("✅ [IA] Opération terminée. En attente de la prochaine commande.")


def monitor_firebase_orders():
    print("🚀 STATION REVPCBAI ACTIVE - PRÊTE POUR LE ROUTAGE (via Firebase)")
    print(f"🎧 URL : {FIREBASE_URL}")
    # 🔗 Nœud unifié avec firebase_daemon.py et index.html
    db.reference('revpcbai_commands').listen(handle_command)


if __name__ == "__main__":
    monitor_firebase_orders()
    # Boucle infinie pour garder le script en vie
    while True:
        time.sleep(1)
