from typing import Final
import telebot
from telebot import types
import data
import start
import buy



token = data.Token()

#getting data from the data.py
BOT_TOKEN = token.get_bot_token()
BOT_USERNAME = token.get_bot_username()


#creating bot
bot = telebot.TeleBot(BOT_TOKEN)


#Commands for telegram '/command'
@bot.message_handler(commands=['start'])
def start_handler(message : types.Message):
    start.start_command(bot, message)

@bot.message_handler(commands=['buy'])
def buy_handler(message : types.Message):
    buy.buy_command(bot, message)

    token_address = buy.token_address_handler(message)
    bot.send_message(message.chat.id, token_address)
    
#Handling queries
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # 'call.data' contains the 'callback_data' from the inline button that was pressed
    if call.data == 'buy_button':
        pass
        # buy.buy_command(bot, types.Message)

        # token_address = token.get_token_address()
        # bot.send_message(types.Message.chat.id, token_address)

print('polling...')
# bot.remove_webhook() # for webhook
bot.polling() #for telegram













# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     welcome_message = '\bWelcome to LeRegularBot on Solana!\
#     \n\nIntroducing the next-level bot crafted for Solana Traders. \
#     Snipe any token right as they launch and trade any token instantly before and after launch'
#     await update.message.reply_text(welcome_message)
    
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     help_message = ''
#     await update.message.reply_text(help_message)

# async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     buy_message = 'Enter a token symbol or address to buy'
#     await update.message.reply_text(buy_message)
#     # update.message.send

# async def sell_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     sell_message = ''
#     await update.message.reply_text(sell_message)


# #Handling messages
# @bot.message_handler(commands=[start_command])
# async def start_page(message, update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # Setting 2 buttons per row
#     markup = InlineKeyboardMarkup(row_width=2)
#     # Creating buttons
#     buy_button = InlineKeyboardButton('Buy', callback_data='buy_button')
#     sell_button = InlineKeyboardButton('Sell', callback_data='sell_button')
#     snipe_button = InlineKeyboardButton('Snipe', callback_data='snipe_button')
#     help_button = InlineKeyboardButton('Help', callback_data='help_button')
#     refresh_button = InlineKeyboardButton('Refresh', callback_data='refresh_button')

#     keyboard_inline = markup.add(buy_button, sell_button, snipe_button, help_button, refresh_button)

#     await bot.send_message(message.chat.id, reply_markup=markup)



# #Responses
# def handle_response(text: str) -> str:
#     response = ''
#     return(response)


# if __name__ == '__main__':
#     print('Starting bot...')
#     app = Application.builder().token(BOT_TOKEN).build()

#     #commands
#     app.add_handler(CommandHandler('start', start_command))
#     app.add_handler(CommandHandler('help', help_command))
#     app.add_handler(CommandHandler('buy', buy_command))
#     app.add_handler(CommandHandler('sell', sell_command))




#     # checking for new user input
#     print('Polling...')
#     app.run_polling(poll_interval=1)



