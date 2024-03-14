import telebot
from telebot import types
import data

token = data.Token()

BOT_TOKEN = token.get_bot_token()
BOT_USERNAME = token.get_bot_username()

bot = telebot.TeleBot(BOT_TOKEN)

def help_message(bot, message : types.Message):
    welcome_message = '<b>Welcome to LeRegularBot on Solana!</b>\
    \n\nIntroducing the next-level bot crafted for Solana Traders. \
    Snipe any token right as they launch and trade any token instantly before and after launch'
    bot.send_message(message.chat.id, welcome_message, parse_mode = 'HTML')