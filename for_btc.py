import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from coinmarketcap import Market
from telegram.ext import (RegexHandler, CommandHandler, ConversationHandler, Handler, MessageHandler, Filters,
                            Updater)
import requests
from bs4 import BeautifulSoup
import botfuncs as funcs


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

CHOOSE, TOP5, BTC, MARKETS, MAIN, REGIME = range(6)

def get_html(site):
    r = requests.get(site)
    return r.text

def parse(html):
    soup = BeautifulSoup(html, 'lxml')

    line = soup.find('div', id="crypto_exchange").find('table', class_='items').find('tbody').find_all('tr')

    markets = []

    for tr in line:
        td = tr.find_all('td')
        markets.append(td[0].text[:-16])

    return markets


def gettin(bot, update, user_data):
    try:
        if user_data['btc'] == 'inline':
            keyboard = [[InlineKeyboardButton("Ціна бітка", callback_data='1'),
                     InlineKeyboardButton("Топ 5", callback_data='2')]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text('Ви перейшли в режим криптовалют. Виберіть дію:', reply_markup=reply_markup)

        else:
            keyboard = [['Ціна бітка'], ['Топ 5'], ['Вихід']]
            kboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            update.message.reply_text('Виберіть дію: ', reply_markup=kboard)
            print('here')
            return CHOOSE

    except KeyError:
        bot.send_message(chat_id=update.message.chat_id, text='Виберіть криптовалютний режим в налаштуваннях')





def button(bot, update, user_data):
    coin = Market()
    if user_data['btc'] == 'inline':
        query = update.callback_query

        if query.data == '0':
            keyboard = [[InlineKeyboardButton("Ціна бітка", callback_data='1'),
                        InlineKeyboardButton("Топ 5", callback_data='2')]]

            reply_markup = InlineKeyboardMarkup(keyboard)

            bot.editMessageText(text="Ви перейшли в режим криптовалют. Виберіть дію: \n",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=reply_markup)

        if query.data == '1':
            keyboard = [[InlineKeyboardButton("Назад", callback_data='0')]]
            data = coin.ticker(1, convert = "USD")
            price = str(data["data"]["quotes"]["USD"]["price"])
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.editMessageText(text="Ціна бітка станом на сьогодні: \n"+price+" USD",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id, reply_markup=reply_markup)

        if query.data == '2':
            user_data['values'] = []
            data = coin.ticker(start = 0, limit = 5, convert = "USD")
            top = data["data"]
            z = list(top.keys())

            for x in z:
                user_data['values'].append(data['data'][str(x)]['name'])
            zboard = []
            for x in user_data['values']:
                zboard.append([InlineKeyboardButton(x, callback_data=x)])
            zboard.append([InlineKeyboardButton("Назад", callback_data='0')])
            reply_markup = InlineKeyboardMarkup(zboard)
            bot.editMessageText(text="Топ 5 криптовалют: \n",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=reply_markup)

        if query.data in user_data['values']:
            var = query.data
            kboard = [[InlineKeyboardButton("Назад", callback_data='2'),InlineKeyboardButton("На головну", callback_data='0')]]
            new_keyboard = InlineKeyboardMarkup(kboard)

            site = 'https://myfin.by/crypto-rates/'
            if str(var) == 'XRP':
                site = 'https://myfin.by/crypto-rates/ripple'
            else:
                site += str(var).lower()

            new_markets = parse(get_html(site))
            result_markets = '\n'.join(new_markets)

            bot.editMessageText(text="Активні біржі для криптовалюти "+str(var)+':\n'+result_markets,
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            reply_markup=new_keyboard)



def choose(bot, update, user_data):
    coin = Market()
    data = coin.ticker(1, convert = "USD")
    price = str(data["data"]["quotes"]["USD"]["price"])
    update.message.reply_text(text="Ціна бітка станом на сьогодні: \n"+price+" USD")
    print('here')

def top(bot, update, user_data):
    coin = Market()
    user_data['values'] = []
    user_data['markets'] = []
    data = coin.ticker(start = 0, limit = 5, convert = "USD")
    top = data["data"]
    z = list(top.keys())

    for x in z:
        user_data['values'].append(data['data'][str(x)]['name'])
        user_data['markets'].append(RegexHandler('^'+str(data['data'][str(x)]['name'])+'$', markets, pass_user_data=True))

    reply_markup = ReplyKeyboardMarkup(user_data['values'])
    string = '\n'.join(user_data['values'])
    bot.send_message(chat_id=update.message.chat_id, text='Топ 5 криптовалют: \n'+string)

def markets(bot, update, user_data):
    text = update.message.text
    if text in user_data['values']:

            site = 'https://myfin.by/crypto-rates/'
            if str(text) == 'XRP':
                site = 'https://myfin.by/crypto-rates/ripple'
            else:
                site += str(text).lower()

            new_markets = parse(get_html(site))
            result_markets = '\n'.join(new_markets)

            update.message.reply_text('Доступні біржі для криптовалюти '+text+'\n'+result_markets)

def exit(bot,update):
    bot.send_message(chat_id= update.message.chat_id, text="Ви вийшли з криптовалютного режиму")
    return ConversationHandler.END


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


pp = BasePersistence()
updater = Updater("TOKEN", persistence=pp)


dp = updater.dispatcher

btc_handler = ConversationHandler(entry_points=[CommandHandler('get_crypto', gettin, pass_user_data=True)],
                                            states={
                                                CHOOSE: [RegexHandler('^Ціна бітка$', choose, pass_user_data=True),
                                                         RegexHandler('^Топ 5$', top, pass_user_data=True),
                                                         RegexHandler('^Вихід$', exit)],

                                                #MARKETS: [user_data['markets']],
                                                #MAIN: []
                                            },
                                          fallbacks=[],
                                  )



