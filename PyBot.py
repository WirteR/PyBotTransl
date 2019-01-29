import telegram
from telegram.ext import  Updater, CommandHandler
from telegram.ext import MessageHandler, Filters,CallbackQueryHandler
from googletrans import Translator
import logging

import botfuncs as funcs
import for_btc as btc

tok = '754612549:AAEewg5s00ru_8QdPAt2GvpFH4GsaU7cSL0'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

if __name__ == "__main__":
    translator = Translator()
    bot = telegram.Bot(token = tok)
    updater = Updater(token = tok)
    disp = updater.dispatcher

    start_handler = CommandHandler('start', funcs.start)
    helper_handler = CommandHandler('help', funcs.helper)
    settings_handler = CommandHandler('settings', funcs.settings)
    get_handler = CommandHandler('get_crypto', btc.gettin)
    ch_handler = MessageHandler(Filters.text, funcs.choose)
    unknown_handler = MessageHandler(Filters.command, funcs.unknown)


    disp.add_handler(ch_handler)
    disp.add_handler(start_handler)
    disp.add_handler(get_handler)
    disp.add_handler(helper_handler)
    disp.add_handler(settings_handler)
    disp.add_handler(CallbackQueryHandler(btc.button))
    disp.add_error_handler(btc.error)
    disp.add_handler(unknown_handler)


    updater.start_polling()

    updater.idle()




