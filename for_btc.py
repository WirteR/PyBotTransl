import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from coinmarketcap import Market
from telegram.ext import RegexHandler, CommandHandler, ConversationHandler
import requests
from bs4 import BeautifulSoup
import botfuncs as funcs


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


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
    if user_data['btc'] == 'inline':
        keyboard = [[InlineKeyboardButton("Ціна бітка", callback_data='1'),
                     InlineKeyboardButton("Топ 5", callback_data='2')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Ви перейшли в режим криптовалют. Виберіть дію:', reply_markup=reply_markup)
    else:
        update.message.reply_text('Wait for updates))')


def button(bot, update, user_data):
    if user_data['btc'] == 'inline':
        query = update.callback_query
        coin = Market()

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
    else:
        update.message.reply_text('Wait for updates))')



def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))

