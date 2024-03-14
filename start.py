import telebot
from telebot import types
import data

token = data.Token()

BOT_TOKEN = token.get_bot_token()
BOT_USERNAME = token.get_bot_username()

bot = telebot.TeleBot(BOT_TOKEN)

def start_command(bot, message : types.Message):
    welcome_message = '<b>Welcome to LeRegularBot on Solana!</b>\
    \n\nIntroducing the next-level bot crafted for Solana Traders. Snipe any token right as they launch and trade any token instantly before and after launch'
    
    # Setting 2 buttons per row
    markup = types.InlineKeyboardMarkup(row_width= 3)

    # Creating buttons
    buy_button = types.InlineKeyboardButton('Buy', callback_data='buy_button')
    sell_button = types.InlineKeyboardButton('Sell', callback_data='sell_button')
    auto_snipe_button = types.InlineKeyboardButton('Auto Snipe', callback_data='auto_snipe_button')
    manual_snipe_button = types.InlineKeyboardButton('Manual Snipe', callback_data='manual_snipe_button')
    scanner_button = types.InlineKeyboardButton('View Scanner', callback_data='scanner_button')
    help_button = types.InlineKeyboardButton('Help', callback_data='help_button')
    settings_button = types.InlineKeyboardButton('Settings', callback_data='settings_button')
    refresh_button = types.InlineKeyboardButton('Refresh', callback_data='refresh_button')

    keyboard_inline = markup.add(buy_button, sell_button, auto_snipe_button, manual_snipe_button,
                                 scanner_button, help_button, settings_button, refresh_button)

    bot.send_message(message.chat.id, welcome_message, reply_markup = markup, parse_mode = 'HTML')