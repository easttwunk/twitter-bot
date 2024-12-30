import os
import time
import tweepy
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Authentifizierung
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Liste der Nutzer, auf deren Posts geantwortet werden soll
nutzer_liste = [
    "iamleocollins", "choker_max", "Ronnbottom", "KingPupSkin1", "hot_germanguy",
    "StevenLee3X", "Pitty4u1", "TillNeuSN", "iamleocollins", "HammerHeinrich",
    "Dupicassoo", "BaghiraOf", "GerMuscle", "kinkytwink24", "marcust088",
    "Snkboy44", "Stony11zoll", "kinkysub_berlin"
]

# Dummy HTTP-Server, um Render zufrieden zu stellen
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Dummy server running.")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def start_dummy_server():
    server = HTTPServer(("0.0.0.0", 10000), DummyHandler)
    print("Dummy server läuft auf Port 10000...")
    server.serve_forever()

# Funktion: Antworte auf den neuesten Tweet eines Nutzers
def antworte_auf_tweet(nutzername, antwort_text, bild_pfad=None):
    try:
        # Abrufen der letzten Tweets des Nutzers
        tweets = api.user_timeline(screen_name=nutzername, count=1)
        for tweet in tweets:
            print(f"Gefundener Tweet von @{nutzername}: {tweet.text}")

            # Antwort senden
            if bild_pfad:
                media = api.media_upload(bild_pfad)
                api.update_status(
                    status=antwort_text,
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True,
                    media_ids=[media.media_id]
                )
            else:
                api.update_status(
                    status=antwort_text,
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            print(f"Antwort gesendet an @{nutzername}!")
    except tweepy.TweepError as e:
        print(f"Fehler beim Antworten auf @{nutzername}: {e}")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")

# Twitter-Bot-Funktionalität
def start_twitter_bot():
    antwort_text = "Hey geiler Style, würd gern beim nächsten Mal dabei sein! Check my profil and DM me for my OF 😊 "  # Antworttext
    bild_pfad = "easttwunk_style.jpg"  # Optional: Pfad zum Bild

    for nutzer in nutzer_liste:
        antworte_auf_tweet(nutzer, antwort_text, bild_pfad)

        # Warten, um API-Limits einzuhalten
        print("Warte 15 Minuten, um API-Limits einzuhalten...")
        time.sleep(900)  # 15 Minuten Pause

# Hauptprogramm
if __name__ == "__main__":
    # Dummy-Server in einem separaten Thread starten
    dummy_thread = threading.Thread(target=start_dummy_server)
    dummy_thread.daemon = True
    dummy_thread.start()

    # Twitter-Bot starten
    start_twitter_bot()
