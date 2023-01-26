# Twitter ELT Pipeline
# -----------------------------------------------------------------------
# Imports
from pymongo import MongoClient
from airflow import DAG
import tweepy
from textblob import TextBlob
import pandas as pd
from airflow.operators.python import PythonOperator
from datetime import timedelta
from datetime import datetime
# -----------------------------------------------------------------------
# Airflow SetUP

# Set default_args dictionary
default_args = {
    # Owner of the DAG
    "owner": "me", 
    # Start time 
    "start_date": datetime.now(), 
    "depends_on_past": False,
    # Retries are disabled
    "retries": 0,
    # If it retries, it waits a tenth of a minute to retry
    "retry_delay": timedelta(minutes=0.1), 
}

# Creating a DAG called TWITTER_MONGO_DAG that is schedule to 
# repeat each minute
dag = DAG(
    "TWITTER_MONGO_DAG",
    default_args=default_args,
    # Runs every minute
    schedule_interval=timedelta(minutes=1)
)
# -----------------------------------------------------------------------
# Function to scrap tweets and store them in Mongo DB
def request_to_mongo():
    # Login Credentials for the Twitter API

    # Set up API credentials for Twitter API
    consumer_key = 'enter-consumer-key-here' 
    consumer_secret = 'enter-consumer-secret-here'
    access_token = 'enter-access-token-here'
    access_token_secret = 'enter-access-token-secret-here'

    # Authenticate using the Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    client = MongoClient(host='host.docker.internal', port=27017) # connecting client to an internal port within docker where airflow is being run

    # Create new Database in MongoDB called "mydatabase"
    db = client['mydatabase']

    # Create the collection in MongoDB for the tweets
    collection = db['tweets']

    # Get the tweets from the OpenAI Twitter account
    searcht = api.search_tweets(q="ChatGPT -filter:retweets", lang='en', count = 100)

    current = []
    # Collect the current tweets in the Mongo DB
    for doc in collection.find():
        current.append(doc['_id'])
    # Search through the new and current tweets to ensure no duplicates are
    # into Mongo
    for tweet in searcht:
        if tweet.id in current:
            pass
        else:
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
# Function to conduct sentiment analysis on the Tweets
def sentimental():

    # Connecting client to an internal port within docker where airflow is being run
    client = MongoClient(host='host.docker.internal', port=27017) 

    # Connecting to the MongoDB
    db = client['mydatabase']

    # Connecting to the "tweets" collection in MongoDB
    collection = db['tweets']

    # Gathering all the data from the database
    data = collection.find()

    # Create lists to store the tweet id, tweet text and date of tweet
    id_list = []
    text_list = []
    date_list = []
    
    # Appenind the id, text and date to lists
    for d in data:
        id_list.append(d['_id'])
        text_list.append(d['text'])
        date_list.append(d['created_at'])

# ---------------------------------------------------------------
# Sentiment Analysis
    # Create lists to store the sentiment scores, tweet text and date of tweet
    sentiment_data_list = []
    text_data_list = []
    date_data_list = []

    # Conduct sentiment analysis on the tweets and store each sentiment score (polarity,subjectivity)
    for i in range(len(text_list)):
        # Text blob handles the sentiment analysis of the tweets
        tweet_blob = TextBlob(text_list[i])
        # Extracting the polarity and subjectivity scores
        polarity, subjectivity = tweet_blob.sentiment

        # Classifying the sentiment (Postive, Negative, Neutral)
        if polarity > 0:
            sentiment = "Positive"
        elif polarity == 0:
            sentiment = "Neutral"
        else:
            sentiment = "Negative"

        # # Storing the sentiment scores, tweet text and tweet dates in a dictionary
        sentiment_data = {"tweet_id": id_list[i], "polarity score": polarity, "sentiment": sentiment, "subjectivity score": subjectivity}
        text_data = {"tweet_id": id_list[i], 'tweet_content': text_list[i]}
        date_data = {"tweet_id": id_list[i], 'tweet_date': date_list[i]}

        sentiment_data_list.append(sentiment_data)
        text_data_list.append(text_data)
        date_data_list.append(date_data)


    # Storing the sentiment scores, tweet text and tweet dates in a dataframe
    sentiment_df = pd.DataFrame(sentiment_data_list)
    text_df = pd.DataFrame(text_data_list)
    date_df = pd.DataFrame(date_data_list)

    # Choose folder path to store the dataframes
    folder_path = 'insert-folder-path-here'

    # Save the DataFrame as a CSV file in the specified folder
    sentiment_df.to_csv(folder_path + '/sentiment_scores.csv', index=False)
    text_df.to_csv(folder_path + '/tweets.csv', index=False)
    date_df.to_csv(folder_path + '/dates.csv', index=False)

# ---------------------------------------------------------------
# Airflow Tasks

# task1: calls the Twitter API and stores the tweets into MongoDB
task1 = PythonOperator(
    task_id = 'twit_mongo',
    python_callable=request_to_mongo,
    provide_context = True,
    dag=dag
)

# task2: extracts the data from the MongoDB and conducts sentiment analysis on the tweets
task2 = PythonOperator(
    task_id = 'sentimental_analysis',
    python_callable=sentimental,
    provide_context = True,
    dag=dag
)

task2.set_upstream(task1)
# ---------------------------------------------------------------
