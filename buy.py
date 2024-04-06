import telebot
from telebot import types
import data
import requests

token = data.Token()

BOT_TOKEN = token.get_bot_token()
BOT_USERNAME = token.get_bot_username()

bot = telebot.TeleBot(BOT_TOKEN)

DEX_API_URL = 'https://api.dexscreener.com/latest/dex/search/?q='
# In-memory storage for token addresses by chat_id
token_address_dict = {}

#comman hander
def buy_command(bot, message : types.Message):
    buy_message = 'Enter a token symbol or address to buy'
    msg = bot.reply_to(message, buy_message)

    bot.register_next_step_handler(msg, token_address_handler)

@bot.message_handler(func= lambda message: message.text is not None and '/' not in message)
def token_address_handler(message : types.Message):
    try:
        chat_id = message.chat.id
        token_address = message.text
        # # Store the token address in the in-memory dictionary
        # token_address_dict[chat_id] = token_address
        response = requests.get(DEX_API_URL + token_address)

        if response.status_code == 200:
            results = response.json()

            if results['pairs']:
                for pair in results['pairs']:
                    # Construct a message with the desired information
                    pair_info = f"Pair: {pair['name']}\nExchange: {pair['exchange']}\nPrice: {pair['price']}\n"
                    bot.send_message(message.chat.id, pair_info)
            else:
                bot.send_message(message.chat.id, "No pairs found.")

        return results
        
    except Exception as e:
        bot.reply_to(message, 'Error Raised')
        # Consider logging the error as well
        print(f"Error: {e}")






# def buy_command(bot, message : types.Message):
#     buy_message = 'Enter a token symbol or address to buy'
#     msg = bot.reply_to(message, buy_message)

#     bot.register_next_step_handler(msg, token_address_handler)

# @bot.message_handler(func= lambda message: message.text is not None and '/' not in message)
# def token_address_handler(message : types.Message) -> str:
#     try:
#         chat_id = message.chat.id
#         token_address = message.text
#         # Store the token address in the in-memory dictionary
#         token_address_dict[chat_id] = token_address

#         # Confirmation message to the user
#         bot.send_message(chat_id, f"Token address '{token_address_dict[chat_id]}' has been stored.")
        
#     except Exception as e:
#         bot.reply_to(message, 'Error Raised')
#         # Consider logging the error as well
#         print(f"Error: {e}")

#     return token_address_dict[chat_id]


        
    
    

    