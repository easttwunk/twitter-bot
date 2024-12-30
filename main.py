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

# Funktion: Poste eine Antwort auf bekannte Tweet-IDs
def antworte_auf_tweet(tweet_id, antwort_text, bild_pfad=None):
    try:
        # Antwort senden
        if bild_pfad:
            media = api.media_upload(bild_pfad)
            api.update_status(
                status=antwort_text,
                in_reply_to_status_id=tweet_id,
                auto_populate_reply_metadata=True,
                media_ids=[media.media_id]
            )
        else:
            api.update_status(
                status=antwort_text,
                in_reply_to_status_id=tweet_id,
                auto_populate_reply_metadata=True
            )
        print(f"Antwort gesendet auf Tweet-ID {tweet_id}!")
    except tweepy.TweepyException as e:
        print(f"Fehler beim Antworten: {e}")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")

# Twitter-Bot-Funktionalität
def start_twitter_bot():
    antwort_text = "Hey, ich bin ein Bot! 😊"  # Antworttext
    bild_pfad = "easttwunk_style.jpg"  # Optional: Pfad zum Bild
    tweet_ids = ["1234567890123456789", "9876543210987654321"]  # Bekannte Tweet-IDs

    for tweet_id in tweet_ids:
        antworte_auf_tweet(tweet_id, antwort_text, bild_pfad)
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
