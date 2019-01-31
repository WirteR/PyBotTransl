from googletrans import Translator

import botfuncs as funcs
import for_btc as btc

import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

import logging

tok = '754612549:AAEewg5s00ru_8QdPAt2GvpFH4GsaU7cSL0'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def main():
    translator = Translator()
    bot = telegram.Bot(token = tok)
    updater = Updater(token = tok)
    disp = updater.dispatcher

    start_handler = CommandHandler('start', funcs.start, pass_user_data=True)
    helper_handler = CommandHandler('help', funcs.helper)
    get_handler = CommandHandler('get_crypto', btc.gettin, pass_user_data=True)
    com_handler = CommandHandler('get', funcs.get, pass_user_data=True)

    ch_handler = MessageHandler(Filters.text, funcs.transl, pass_user_data=True)
    unknown_handler = MessageHandler(Filters.command, funcs.unknown)

    disp.add_handler(start_handler)
    disp.add_handler(get_handler)
    disp.add_handler(helper_handler)
    disp.add_handler(funcs.conv_handler)
    disp.add_handler(com_handler)

    disp.add_handler(CallbackQueryHandler(btc.button, pass_user_data=True))
    disp.add_error_handler(btc.error)
    disp.add_handler(ch_handler)
    disp.add_handler(unknown_handler)


    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
