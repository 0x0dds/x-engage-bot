import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # 👈 Add this to .env

# Validate all
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN]):
    print("❌ Missing credentials. Check your .env file.")
    exit()

# Setup v2 client for SEARCH
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Setup v1.1 API for LIKE
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api_v1 = tweepy.API(auth)

# Keyword and settings
keyword = "Newton"
max_likes = 5

print(f"🔍 Searching for tweets containing: {keyword}")

try:
    response = client.search_recent_tweets(
        query=keyword,
        max_results=max_likes,
        tweet_fields=["author_id", "lang"]
    )

    tweets = response.data

    if not tweets:
        print("⚠️ No tweets found.")
    else:
        for tweet in tweets:
            print(f"📄 {tweet.text[:60]}...")
            try:
                api_v1.create_favorite(tweet.id)
                print("✅ Liked it!")
            except Exception as e:
                print(f"❌ Error liking tweet {tweet.id}: {e}")

except Exception as e:
    import traceback
    print("🚫 Failed during search or like process:")
    traceback.print_exc()