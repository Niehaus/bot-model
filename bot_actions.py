"""
author: Bárbara Boechat
date: 29/04/2021

Main Actions for a Twitter Bot:
    - Follow  - Unfollow
    - Retweet - Tweet (?)
    - Comment (?)

"""

import tweepy


class BotModel:
    def __init__(self, tokens):
        self.bot_name = tokens["bot_name"]
        self.bearer_token = tokens["bearer_token"]
        self.access_token = tokens["access_token"]
        self.access_token_secret = tokens["access_token_secret"]
        self.api_key = tokens["api_key"]
        self.api_secret_key = tokens["api_secret_key"]
        self.api = tweepy.API(self.authenticate())

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret_key)
        auth.set_access_token(self.access_token, self.access_token_secret)

        return auth

    def tweet(self, msg):
        """ Tweet próprio na timeline """
        self.api.update_status(
            f"{msg}\n"
            f"- Tweet from {self.bot_name}"
        )

    def reply(self, msg, tweet_id):
        """ Responde a um tweet """
        self.api.update_status(
            f"{msg}\n",
            in_reply_to_status_id=tweet_id
        )

    def follow(self, screen_name, user_id=None):
        """ Cria uma amizade entre usuários (follow) """
        if not user_id:
            user_id = self.api.get_user(screen_name).id
        self.api.create_friendship(user_id)

    def unfollow(self, screen_name, user_id=None):
        """ Destroi uma amizade entre usuários (follow) """
        if not user_id:
            user_id = self.api.get_user(screen_name).id
        self.api.destroy_friendship(user_id)

    def retweet(self, tweet_id, msg=None):
        """ Cria um retweet com ou sem comentário, contudo, retweet com
        comentário apenas é possível realizando embed do rt no seu tweet
        pelo tweepy, com a v2 da api talvez seja possível """

        if not msg:
            self.api.retweet(tweet_id)
        else:
            embedded_url = self.api.get_status(tweet_id).entities['media'][0]['url']
            self.api.update_status(f"{msg} {embedded_url}")
