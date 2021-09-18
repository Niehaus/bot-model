import configparser

from bot.bot_actions import *
from bot.db_handler import DbConnection, TwitterItem

if __name__ == '__main__':
    # temporary config getter will be replaced by gitsecrets
    config = configparser.RawConfigParser()
    config.sections()
    config.read('config.cfg')

    # access tokens from developer.twitter.com
    tokens = {
        "bot_name": "Bot Model Test 02",
        "bearer_token": config['DEFAULT']['bearer_token'],
        "access_token": config['DEFAULT']['access_token'],
        "access_token_secret": config['DEFAULT']['access_token_secret'],
        "api_key": config['DEFAULT']['api_key'],
        "api_secret_key": config['DEFAULT']['api_secret_key']
    }

    # actions standard instance
    bot = BotActions(tokens)
    twitter_data = bot.myself_data()
    connection_pass = config['DEFAULT']['mongo_password']
    db = DbConnection(connection_pass, {'tag': twitter_data.screen_name})
    db.bot_overview()
    db.update_account_info(twitter_data)

    tweet = TwitterItem("12", "algo", "hoje", "sou eu")
    print(tweet.__dict__)
    # database_access.server_status()

    # currently working actions of the actions model
    # actions.tweet("hello again :D")
    # actions.follow(1159210901825904640)
    # actions.unfollow('joaoluizpedrosa')
    # actions.reply('actions: reply test', 1391920122265231364)
    # actions.retweet(1389325211603017729)

    # dm examples
    # user_to_respond, message_data = bot.dm.latest_recived_dm()
    # actions.dm.send_dm(user_to_respond)
