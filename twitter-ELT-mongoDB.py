# Twitter ELT Pipeline
# -----------------------------------------------------------------------
# Imports
import tweepy
from pprint import pprint
from pymongo import MongoClient
# -----------------------------------------------------------------------
# Login Credentials for the Twitter API

# Set up API credentials for Twitter API
consumer_key = 'Add-Twitter-Consumer-Key-Here'
consumer_secret = 'Add-Twitter-Consumer-Secret-Here'
access_token = 'Add-Twitter-Access-Token-Here'
access_token_secret = 'Add-Twitter-Access-Token-Secret-Here'

# Authenticate using the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# -----------------------------------------------------------------------
# Create MongoDB Client
client = MongoClient('mongodb://localhost:27017/')

# Create new Database in MongoDB called "mydatabase"
db = client['mydatabase']
print(client.list_database_names())

# Create the collection in MongoDB for the tweets
collection = db['tweets']
# -----------------------------------------------------------------------
# Get the tweets from the OpenAI Twitter account
searcht = api.search_tweets(q="ChatGPT", lang='en', count = 200)

# Parse through  all the tweets and collect as much information as possible
for tweet in searcht:
    # Create a dictionary for each tweet
    tweet_info = {}
    # Tweet ID
    tweet_info["id"] = tweet.id
    # Date the Tweet was tweeted
    tweet_info["created_at"] = tweet.created_at
    # Text of the Tweet
    tweet_info["text"] = tweet.text
    # ID of the user that Tweeted the tweet
    tweet_info["user_id"] = tweet.user.id
    # Location of the user that tweeted
    tweet_info["location"] = tweet.user.location
    # FOllwoer count of the user that tweeted
    tweet_info["followers_count"] = tweet.user.followers_count
    # The number of tweets the user has tweeted
    tweet_info["statuses_count"] = tweet.user.statuses_count
    # When the user created their account
    tweet_info["user_creation"] = tweet.user.created_at
    # The hashtags included in the tweet
    tweet_info["hashtags"] = [hashtag["text"] for hashtag in tweet.entities.get("hashtags")]
    # URLs in the tweet
    tweet_info["urls"] = [url["expanded_url"] for url in tweet.entities.get("urls")]
    # Users mentioned in the tweet
    tweet_info["user_mentions"] = [user_mention["screen_name"] for user_mention in tweet.entities.get("user_mentions")]
    # Whether the tweet contains media
    tweet_info["media"] = [media.media_url for media in tweet.entities.get("media")] if hasattr(tweet, "media") else None
    # Whether the tweet contains a poll
    tweet_info["polls"] = [poll.options for poll in tweet.polls()] if hasattr(tweet, "polls") else None
    # The number of retweets the tweet has
    tweet_info["retweet_count"] = tweet.retweet_count
    # The  number  of likes the tweet has
    tweet_info["favorite_count"] = tweet.favorite_count
    
    # Inserting the data into the database in MongoDB
    collection.insert_one(tweet_info)
# -----------------------------------------------------------------------
# Show a record in our mongo Database
data_example = collection.find_one()
pprint(data_example)
# -----------------------------------------------------------------------
# Check the data in mongoDB!