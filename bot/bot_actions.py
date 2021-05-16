"""
author: Bárbara Boechat
date: 29/04/2021

Main Actions for a Twitter Bot:
    - Follow  - Unfollow
    - Retweet - Tweet (?)
    - Comment (?)

"""

import tweepy


class BotActions:
    def __init__(self, tokens):
        self.__bearer_token = tokens["bearer_token"]
        self.__access_token = tokens["access_token"]
        self.__access_token_secret = tokens["access_token_secret"]
        self.__api_key = tokens["api_key"]
        self.__api_secret_key = tokens["api_secret_key"]
        self.api = tweepy.API(self.authenticate())

        self.bot_name = tokens["bot_name"]
        self.dm = self.DmHandler(self.api, self.myself_data())
        self.identity = "brainnn"

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.__api_key, self.__api_secret_key)
        auth.set_access_token(self.__access_token, self.__access_token_secret)

        return auth

    def myself_data(self):
        """ Dados do perfil autenticado """
        return self.api.me()

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

    def block(self, screen_name, id_to_block=None):
        """ Block a user by its id or screen_name """
        if not id_to_block:
            id_to_block = self.api.get_user(screen_name).id
        self.api.create_block(id_to_block)

    def unblock(self, screen_name, id_to_block=None):
        """ Unblock a user by its id or screen_name """
        if not id_to_block:
            id_to_block = self.api.get_user(screen_name).id
        self.api.destroy_block(id_to_block)

    class DmHandler:
        def __init__(self, owner, owner_data):
            self.owner = owner
            self.my_id = owner_data.id
            self.dms = self.dms_list()

        def dms_list(self):
            return self.owner.list_direct_messages()

        def latest_recived_dm(self):
            """
            Gets pertinent data of the last recived dm in the actions
            twitter account currently connected to the api.

            :return: Id of the dm that the last message came from,
                    so it can be responded and the data of the last message,
                    as its text, hashtags, symbols or mentions that could existis
                    in the message body.
            """
            for dm in self.dms:
                if int(dm.message_create['target']['recipient_id']) == self.my_id:
                    return dm.id, dm._json["message_create"]["message_data"]

        def send_dm(self):
            ...

        def send_img_dm(self):
            ...
