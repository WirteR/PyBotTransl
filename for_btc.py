import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from coinmarketcap import Market

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

values = []

def gettin(bot, update):
    keyboard = [[InlineKeyboardButton("Ціна бітка", callback_data='1'),
                 InlineKeyboardButton("Топ 5", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Ви перейшли в режим криптовалют. Виберіть дію:', reply_markup=reply_markup)


def button(bot, update):
    global values
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
        values = []
        data = coin.ticker(start = 0, limit = 5, convert = "USD")
        top = data["data"]
        z = list(top.keys())
        for x in z:
            values.append(data['data'][str(x)]['name'])
        zboard = []
        for x in values:
            zboard.append([InlineKeyboardButton(x, callback_data=x)])
        zboard.append([InlineKeyboardButton("Назад", callback_data='0')])
        reply_markup = InlineKeyboardMarkup(zboard)
        bot.editMessageText(text="Топ 5 криптовалют: \n",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=reply_markup)

    if query.data in values:
        var = query.data
        kboard = [[InlineKeyboardButton("Назад", callback_data='2'),]]
        new_keyboard = InlineKeyboardMarkup(kboard)
        bot.editMessageText(text="Ви вибрали "+str(var),
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            reply_markup=new_keyboard)




def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))