import telegram
from telegram.ext import  Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from googletrans import Translator
import logging

tok = '731565223:AAFMQr3wREQFrhU6Zd0k3LLJkWdhCbyZh_8'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
res = 'en'

translator = Translator()

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Цей бот призначений для швидкого перекладу ваших слів на англійську. "
                                                          "Щоб дізнатись більше - введіть /help Приємного користування!")

def helper(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Бот для перекладу на англійську. Developed by Kravets')

def settings(bot, update):
    custom_keyboard = [['Мова для перекладу']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id = update.message.chat_id, text="Виберіть потрібне налаштування:", reply_markup=reply_markup)

def choose(bot, update):
    global res
    if update.message.text == 'Мова для перекладу':
        custom_keyboard = [['English'],['Deutech'],['France']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id = update.message.chat_id, text="Виберіть потрібну мову:", reply_markup=reply_markup)

    elif update.message.text == 'English':
            bot.send_message(chat_id = update.message.chat_id, text="Мову змінено на англійську!", reply_markup=telegram.ReplyKeyboardRemove())
            res = 'en'

    elif update.message.text == 'Deutech':
            bot.send_message(chat_id = update.message.chat_id, text="Мову змінено на німецьку!", reply_markup=telegram.ReplyKeyboardRemove())
            res = 'de'
    elif update.message.text == 'France':
            bot.send_message(chat_id = update.message.chat_id, text="Мову змінено на французьку!", reply_markup=telegram.ReplyKeyboardRemove())
            res = 'fr'
    else:
        returning = str(update.message.text)
        result = translator.translate(returning, dest = res)
        bot.send_message(chat_id=update.message.chat_id, text=result.text)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text = "Вибачте, команди не існує")
