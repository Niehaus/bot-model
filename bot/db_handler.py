"""
author: Bárbara Boechat
date: 29/04/2021

Main Bot Actions Log Generator
"""

from datetime import datetime
from pprint import pprint

from pymongo import MongoClient


class TwitterItem:
    def __init__(self, id, content, data, owner):
        self.id = id
        self.content = content
        self.data = data
        self.owner = owner


class DbConnection:
    def __init__(self, password, bot):
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
        print(bot['tag'])
        bot_looked = self.db.Bots.find_one({"tag": bot['tag']})
        if bot_looked is None:
            try:
                bot['followers'] = 0
                bot['following'] = 0
                bot['bio'] = ""
                bot['last_update'] = datetime.now()
                result = self.db.Bots.insert_one(bot)
                # self.db.Bots.create_index([('tag', 1)], unique=True)
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
        pprint(twitter_data)
        # followers = twitter_data.entities['followers_count']
        # following = twitter_data.entities['friends_count']
        # bio = twitter_data.description
        # profile_pic = twitter_data.entities['profile_image_url']
        # print(followers, following, bio, profile_pic)

        ...


class LogHandler:
    def __init__(self, log_info, date):
        self.log_info = log_info
        self.date = date

    def comment_log(self):
        ...

    def follow_log(self):
        # date, followers_count, is_follow
        print(f"Follow {self.log_info.follow} at {self.date}")

    def daily_follow_log(self):
        ...
