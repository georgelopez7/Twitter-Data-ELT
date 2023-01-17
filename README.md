# Twitter Data ELT

![MicrosoftTeams-image_2](https://user-images.githubusercontent.com/71076769/212994427-f25e9aa8-e181-4e61-b3ce-1790deec8e60.png)

> ELT Pipeline for tweets including ChatGPT, loaded into MongoDB in preparation for sentiment analysis. 

---

### Table of Contents

- [Description](#description)
    
    -  [Technologies & Softwares](#technologies)

- [Database](#database)

    -  [Data Example](#data-example) 
- [Author Info](#author-info)

---

## Description

In this project, we are building an ELT (Extract, Load and Transform) pipeline that utilizes the Twitter API to gather tweets containing the word "ChatGPT". The tweets are then parsed to extract various attributes such as the tweet text, user information, and date of tweet. These attributes are collected and loaded into a MongoDB database. 

The collected data will be used to conduct sentiment analysis on tweets including ChatGPT by applying natural language processing techniques to determining the overall sentiment (positive, neutral, or negative) towards ChatGPT.

### Technologies and Softwares

- Python
    - **tweepy** package
    
        Used to interact  with the Twitter API and collect the tweets.
    - **pyMongo** package

        Used to interact with MongoDB with Python.
    - **textBlob** package

        ADD DESCRIPTION HERE!!

- MongoDB
    
    Used  MongoDB to load and store the collected data from the Twitter API

[Back To The Top](#twitter-data-elt)

---

## Database

Each tweet has a series of attributes extracted and stored within the MongoDB database. Below is the list of attribues:

Attribute | Description 
--- | --- 
id | unique id of tweet 
created_at | time tweet created  
text | content of tweet  
user_id | unique id of the user  
location | user location  
followers_count | how many followers the user has  
statuses_count | how many tweets the user posted  
user_creation | when user created  
hashtags | what hashtags are in the tweet  
urls | what urls are in the tweet
user_mentions | what users the tweet mentions  
media | whether tweet has media 
polls | whether tweet has polls
retweet_count | number of times the tweet has been retweeted  
favorite_count | number times the tweet has been liked (favourited)

### Data Example


Below you can see an entry within the MongoDB database with all the attributes listed above:

```
{'_id': ObjectId('63c67923b4b07626386406fc'),
 'created_at': datetime.datetime(2023, 1, 17, 10, 31, 59),
 'favorite_count': 0,
 'followers_count': 366,
 'hashtags': [],
 'id': 1615295862728523778,
 'location': 'Greater Accra, Ghana',
 'media': None,
 'polls': None,
 'retweet_count': 1033,
 'statuses_count': 1619,
 'text': 'RT @MrSumitBindra: ChatGPT is Most Powerful Tool. \n'
         '\n'
         "But 99% of people don't know how to build a Business and make money "
         'using it.\n'
         '\n'
         "That's w…",
 'urls': [],
 'user_creation': datetime.datetime(2018, 3, 14, 10, 49, 46),
 'user_id': 973873816358342657,
 'user_mentions': ['MrSumitBindra']}
```

[Back To The Top](#twitter-data-elt)

---

## Author Info

LinkedIn - [George Lopez](https://www.linkedin.com/in/george-benjamin-lopez/)

LinkedIn - [Jasmine Albert](https://www.linkedin.com/in/jasmine-albert-99029b207/)

LinkedIn - [Matias Sanchez Wilson](https://www.linkedin.com/in/matiassanchezwilson/)

LinkedIn - [Asfia Hossoin](https://www.linkedin.com/in/asfia-hossoin-9521b6243/)

[Back To The Top](#twitter-data-elt)
