import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def fetch_disaster_tweets(keyword="earthquake", max_results=10):
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    query = f"{keyword} -is:retweet lang:en"
    tweets = client.search_recent_tweets(query=query, max_results=max_results)

    alerts = []
    if tweets.data:
        for tweet in tweets.data:
            alerts.append({
                "location": "Twitter",  # Can use NLP or geotagging later
                "text": tweet.text[:100] + "...",
                "coordinates": None,
                "timestamp": tweet.created_at if hasattr(tweet, "created_at") else None
            })
    
    return alerts
