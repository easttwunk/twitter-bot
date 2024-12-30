import os
import tweepy

# Authentifizierung mit Umgebungsvariablen
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Verbindung mit der Twitter-API herstellen
auth = tweepy.OAuthHandler(JJcKfRWumygxBP30eCRkMFLXW, 2YI0zQ67OKJEKqEeKapVkxMDqOhgh47Boga9YDUT6i8NTFgY7Y)
auth.set_access_token(1608430728630370304-5riCdvr6xs5lvKmhFHWvHxpAxxGMnP, K2mFGKc8EohUQDvH2D3yVileiiKZNEpeINHHPC1SB2MQ7)
api = tweepy.API(auth)

# Funktion: Antwort auf einen Tweet
def antworten(tweet_id, text):
    try:
        api.update_status(
            status=text,
            in_reply_to_status_id=tweet_id,
            auto_populate_reply_metadata=True
        )
        print(f"Antwort gesendet: {text}")
    except Exception as e:
        print(f"Fehler beim Antworten: {e}")

# Funktion: Tweets mit bestimmten Hashtags suchen und darauf antworten
def suche_und_antworten(hashtag, antwort_text):
    try:
        # Tweets suchen
        tweets = api.search_tweets(q=hashtag, count=5, result_type="recent")
        for tweet in tweets:
            print(f"Gefundener Tweet: {tweet.text} von @{tweet.user.screen_name}")
            antworten(tweet.id, antwort_text)
    except Exception as e:
        print(f"Fehler beim Suchen von Tweets: {e}")

# Hauptfunktion
def main():
    hashtag = "#BeispielHashtag"  # Ersetze durch deinen Hashtag
    antwort_text = "Das ist eine automatische Antwort auf deinen Tweet!"  # Ersetze durch deinen Antworttext

    while True:
        print(f"Suche nach Tweets mit dem Hashtag {hashtag}...")
        suche_und_antworten(hashtag, antwort_text)
        print("Warte 60 Sekunden...")
        time.sleep(60)  # Wartezeit zwischen den Suchvorgängen

# Startpunkt des Programms
if __name__ == "__main__":
    main()
