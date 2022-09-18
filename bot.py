from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from datetime import datetime
from handlers import greet_user, talk_to_me, guess_number, send_cat_picture, user_coordinates
import settings

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    encoding='utf-8')

def main():
    mybot = Updater(settings.API_KEY, use_context=True,)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))

    logging.info(f"{datetime.today()} Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
