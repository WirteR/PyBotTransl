import telegram
from telegram.ext import  Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from googletrans import Translator
import logging

tok = '754612549:AAEewg5s00ru_8QdPAt2GvpFH4GsaU7cSL0'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Цей бот призначений для швидкого перекладу ваших слів на англійську. "
                                                          "Щоб дізнатись більше - введіть /help Приємного користування!")

def helper(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Бот для перекладу на англійську. Developed by Kravets')

def echo(bot, update):
    returning = str(update.message.text)
    result = translator.translate(returning)
    bot.send_message(chat_id=update.message.chat_id, text=result.text)


translator = Translator()
bot = telegram.Bot(token = tok)
updater = Updater(token = tok)
disp = updater.dispatcher

start_handler = CommandHandler('start', start)
helper_handler = CommandHandler('help', helper)
echo_handler = MessageHandler(Filters.text, echo)

disp.add_handler(echo_handler)
disp.add_handler(start_handler)
disp.add_handler(helper_handler)



updater.start_polling()




