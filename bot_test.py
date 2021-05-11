from bot_actions import *
import configparser


if __name__ == '__main__':

    # temporary config getter will be replaced by gitsecrets
    config = configparser.RawConfigParser()
    config.sections()
    config.read('config.cfg')

    # access tokens from developer.twitter.com
    tokens = {
        "bot_name": "Bot Model Test 01",
        "bearer_token": config['DEFAULT']['bearer_token'],
        "access_token": config['DEFAULT']['access_token'],
        "access_token_secret": config['DEFAULT']['access_token_secret'],
        "api_key": config['DEFAULT']['api_key'],
        "api_secret_key": config['DEFAULT']['api_secret_key']
    }

    # bot standard instance
    bot = BotModel(tokens)

    # currently working actions of the bot model
    # bot.tweet("hello again :D")
    # bot.follow(1159210901825904640)
    # bot.unfollow('joaoluizpedrosa')
    # bot.reply('bot: reply test', 1391920122265231364)
    # bot.retweet(1389325211603017729)
