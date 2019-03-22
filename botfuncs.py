from googletrans import Translator
import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import RegexHandler, ConversationHandler, CommandHandler
import for_btc as btc

tok = '731565223:AAFMQr3wREQFrhU6Zd0k3LLJkWdhCbyZh_8'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
res = 'en'

translator = Translator()
CHOOSE, LAST, CHANGE = range(3)

markup = ReplyKeyboardMarkup([['Вибір мови'], ['Криптовалютний режим'], ['Вихід'], ], one_time_keyboard=True)   #for lang settings

markap = ReplyKeyboardMarkup([['Відображення в режимі inline'], ['Відображення в режимі клавіатури']],          #for btc settings
                             one_time_keyboard=True)

def start(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Цей бот призначений для швидкого перекладу ваших слів на англійську. ")
    user_data['lan'] = 'en'
    user_data['btc'] = 'reply'


def helper(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Бот для перекладу на англійську. Developed by Kravets')


def get_lan(user_data):
    k = user_data['lan']
    return k


def settings(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Виберіть налаштування:", reply_markup=markup)
    return LAST


def last(bot, update, user_data):
    reply_keyboard = [['English'], ['Deutech'], ['France']]
    user_data['langs'] = reply_keyboard
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Виберіть потрібну мову:", reply_markup=markup)

    return CHOOSE


def choose(bot, update, user_data):
    text = update.message.text
    #if text in user_data['langs']:
    if text == 'France':
        user_data['lan'] = 'fr'

    elif text == 'Deutech':
        user_data['lan'] = 'de'

    elif text == 'English':
        user_data['lan'] = 'en'

    update.message.reply_text('Ви вибрали ' + text, reply_markup=markup)
    return LAST

    #else:
        #update.message.reply_text('Невідома команда', reply_markup=user_data['langs'])
        #return CHOOSE


def cancel(bot, update):
    update.message.reply_text('Ви вийшли з налаштувань')
    return ConversationHandler.END


def get(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text=user_data['lan']+user_data['btc'])


def transl(bot, update, user_data):
    returning = str(update.message.text)
    try:
        result = translator.translate(returning, dest=user_data['lan'])
        bot.send_message(chat_id=update.message.chat_id, text=result.text)
    except KeyError:
        bot.send_message(chat_id=update.message.chat_id, text="Виберіть мову перекладу в налаштуваннях")

def choose_regime(bot, update):
    update.message.reply_text('Виберіть режим: ', reply_markup=markap)

    return CHANGE

def set_regime(bot, update, user_data):
    text = update.message.text
    if text == 'Відображення в режимі inline':
        user_data['btc'] = 'inline'
    else:
        user_data['btc'] = 'reply'

    update.message.reply_text('Ви перейшли в режим ' + user_data['btc'], reply_markup=markup)

    return LAST

def cnc(bot, update):
    pass


def unknown(bot, update):
    if update.message.text == '/settings':
        bot.send_message(chat_id=update.message.chat_id, text="Ви вже вибрали налаштування")

    elif update.message.text == '/get_crypto':
        bot.send_message(chat_id=update.message.chat_id, text="Ви вже в режимі криптовалют")

    else:
        bot.send_message(chat_id=update.message.chat_id, text="Вибачте, команди не існує")



conv_handler = ConversationHandler(entry_points=[CommandHandler('settings', settings)],
                                   states={
                                       LAST: [RegexHandler('^Вибір мови$', last, pass_user_data=True),
                                                RegexHandler('^Криптовалютний режим$', choose_regime),
                                                RegexHandler('^Вихід$', cancel)],

                                       CHOOSE: [RegexHandler('^(English|Deutech|France)$', choose, pass_user_data=True)],

                                       CHANGE: [RegexHandler('^(Відображення в режимі inline|Відображення в режимі клавіатури)$', set_regime,
                                                pass_user_data=True)]
                                   },
                                   fallbacks=[]
                                   )
