"""
author: Bárbara Boechat
date: 29/04/2021

Main Bot Actions Log Generator
"""

from datetime import datetime
from pprint import pprint

from pymongo import MongoClient


class Tweet:
    def __init__(self, content, owner):
        self.content = content
        self.owner = owner
        self.creation_date = datetime.now()


class LogHandler:
    def __init__(self):
        self.client = None
        self.db = None
        self.botId = None
        self.tag = ""

        self.acumulate_tweets = []
        self.acumulate_retweets = []

    def establish_connection(self, password, bot):
        """
        Establish the connection with MongoDb by setting
        this users password and the current bot in action.

        :param password: MongoDb users password
        :param bot: Current bot in action defined by the script.
        """
        self.client = MongoClient(
            f"mongodb+srv://barbara:{password}@cluster0.ntis3.mongodb.net/LogHandler?retryWrites=true&w=majority",
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        self.db = self.client.LogHandler
        self.botId = self.setup_bot(bot)
        self.tag = bot['tag']

    def server_status(self):
        # Show the Server Status of Mongo Atlas Cluster
        server_status = self.db.command("serverStatus")
        pprint(server_status)

    def setup_bot(self, bot):
        bot_looked = self.db.Bots.find_one({"tag": bot['tag']})
        if bot_looked is None:
            try:
                bot['followers'] = []
                bot['following'] = []
                bot['bio'] = ""
                bot['profile_pic'] = ""
                result = self.db.Bots.insert_one(bot)
                # self.db.Bots.create_index([('tag', 1)], unique=True) # Create index for twitter tags
                return result.inserted_id
            except Exception as e:
                print(e, '\n')
                print(f"{bot['tag']} já cadastrado. Tente um Identificador diferente.")
        else:
            return bot_looked.get('_id')

    def bot_overview(self):
        print(f"Twitter Tag: {self.tag} \nMongo Id: {self.botId}")

    def update_account_info(self, twitter_data):
        """
            Every time that the bot runs it has to update
            its followers and following numbers for keeping
            track of them.
            :return:
        """
        followers = {
            "followers_number": twitter_data.followers_count,
            "updated_date": datetime.now()
        }

        following = {
            "following": twitter_data.friends_count,
            "updated_date": datetime.now()
        }
        bio = twitter_data.description
        profile_pic = twitter_data.profile_image_url

        self.db.Bots.update({"tag": self.tag}, {
            '$set': {'bio': bio, 'profile_pic': profile_pic},  # Set variables values
            '$push': {'followers': followers, 'following': following}  # Adds items to arrays
        })

    def tweets_logs(self):
        """
            Format all the tweets that have been acumulated by the bot actions:
             The specific format in this function will be de Tweet format,
             so the content is the most
             relevant thing about this model.
        """
        tweets = []
        for tweet in self.acumulate_tweets:
            tweets.append(Tweet(tweet['content'], self.botId).__dict__)
        self.db.Tweets.insert_many(tweets)

    def tweet_log(self, content):
        """
        Log to the tweets collection one single tweet its text content.

        :param content: Text of a tweet
        """
        tweet = Tweet(content, self.botId).__dict__
        self.db.Tweets.insert_one(tweet)

    def comment_log(self):
        ...

    def follow_log(self):
        # date, followers_count, is_follow
        ...

    def daily_follow_log(self):
        ...
