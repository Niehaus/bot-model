import configparser

from bot.bot_actions import *
from bot.db_handler import LogHandler

if __name__ == '__main__':
    # temporary config getter will be replaced by gitsecrets
    config = configparser.RawConfigParser()
    config.sections()
    config.read('config.cfg')

    # access tokens from developer.twitter.com and MongoDb password
    connection_pass = config['DEFAULT']['mongo_password']
    bot_tag = config['DEFAULT']['bot_tag']

    tokens = {
        "bot_name": "Automation Teste 02",
        "tag": bot_tag,
        "connection_pass": connection_pass,
        "bearer_token": config['DEFAULT']['bearer_token'],
        "access_token": config['DEFAULT']['access_token'],
        "access_token_secret": config['DEFAULT']['access_token_secret'],
        "api_key": config['DEFAULT']['api_key'],
        "api_secret_key": config['DEFAULT']['api_secret_key']
    }

    # actions standard instance
    logger = LogHandler()
    bot = BotActions(tokens, logger)
    twitter_data = bot.myself_data()
    # currently working actions of the actions model
    print("Getting the tweet done!")
    bot.tweet("funciona logo porra")

    print("Logging....")
    logger.establish_connection(connection_pass, {'tag': bot_tag})
    # logger.server_status()
    logger.bot_overview()
    logger.update_account_info(twitter_data)

    logger.tweets_logs()
    print("All gooood!")


    # actions.follow(1159210901825904640)
    # actions.unfollow('joaoluizpedrosa')
    # actions.reply('actions: reply test', 1391920122265231364)
    # actions.retweet(1389325211603017729)

    # dm examples
    # user_to_respond, message_data = bot.dm.latest_recived_dm()
    # actions.dm.send_dm(user_to_respond)
