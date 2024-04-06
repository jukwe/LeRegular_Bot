import telebot
from telebot import types
import telebot.formatting as tb_format
import data
import start
import requests
import tgFormat
# import buy
#imports for web3
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from mnemonic import Mnemonic


token = data.Token()

#getting data from the data.py
BOT_TOKEN = token.get_bot_token()
BOT_USERNAME = token.get_bot_username()

#creating bot
bot = telebot.TeleBot(BOT_TOKEN)


DEX_API_URL = 'https://api.dexscreener.com/latest/dex/search/?q='
# Connect to the Solana network
SOLANA_CLIENT = Client("https://api.devnet.solana.com") # https://api.mainnet-beta.solana.com

#Commands for telegram '/command'
@bot.message_handler(commands=['start']) # start command
def start_command(message):
    keypair = create_wallet()
    account_address = str(keypair.pubkey())
    copy_account_address = "Wallet Address: <code>" + account_address + "</code>" #tap to copy string format
    account_balance = get_account_balance(keypair)
    welcome_message = 'Welcome to LeRegularBot on Solana!\n'
    balance_message = f'\nWallet Balance: {account_balance} SOL'
    
    
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

    bot.send_message(message.chat.id, welcome_message + copy_account_address + balance_message, reply_markup = markup, parse_mode = 'HTML')


    

@bot.message_handler(commands=['buy']) #buy command
def buy_command(message):
    # buy.buy_command(bot, message)

    buy_message = 'Enter a token symbol or address to buy'
    # msg = bot.reply_to(message, buy_message)
    msg = bot.send_message(message.chat.id, buy_message)

    bot.register_next_step_handler(msg, buy_page)
    
# searching for tokens
def dex_token_search(message):
    try:
        chat_id = message.chat.id
        user_token_address = message.text
        # GET request for api
        response = requests.get(DEX_API_URL + user_token_address)

        # Checking if connection made
        if response.status_code == 200:
            # creating dict of info request
            results = response.json()

            # print(results, end='\n\n')
            if results['pairs']:
                token_price = None
                token_liquidity = None
                price_change_5_min = None
                price_change_1_hour = None
                price_change_24_hour = None


                for pair in results['pairs']:                    
                    # Dealing with duplicate key issue for json dict 
                    if all(var is None for var in (token_price, token_liquidity, price_change_5_min, price_change_1_hour, price_change_24_hour)):
                        #getting the values from the baseToken dict
                        token_address = pair['baseToken'].get('address')
                        # copy_token_address = "`" + token_address + "`" #tap to copy string format
                        token_name = pair['baseToken'].get('name')
                        token_symbol = pair['baseToken'].get('symbol')
                        # getting the price # This is duplicate keys start
                        token_price = pair['priceUsd']
                        token_liquidity = pair['liquidity'].get('usd')
                        # formatted_liquidity, liquidity_suffix = tgFormat.format_prices(token_liquidity) # Formatting the liquidity ex: 1.1M
                        price_change_5_min = pair['priceChange'].get('m5')
                        price_change_1_hour = pair['priceChange'].get('h1')
                        price_change_24_hour = pair['priceChange'].get('h24')
                return token_address, token_name, token_symbol, token_price,token_liquidity, price_change_5_min, price_change_1_hour, price_change_24_hour
            else:
                bot.send_message(chat_id, "No pairs found or 'pairs' key is missing in the response.")

        else:
            bot.send_message(chat_id, f"Failed to retrieve data, status code: {response.status_code}")
        # return results
        
    except Exception as e:
        bot.reply_to(message, 'An error occurred while processing your request.')
        # Consider logging the error as well
        print(f"Error: {e}")

def buy_page(message):
    chat_id = message.chat.id
    token_address, token_name, token_symbol, token_price, token_liquidity,\
        price_change_5_min, price_change_1_hour, price_change_24_hour = dex_token_search(message)
    copy_token_address = "<code>" + token_address + "</code>\n" #tap to copy string format
    formatted_liquidity, liquidity_suffix = tgFormat.format_prices(token_liquidity) # Formatting the liquidity ex: 1.1M
    pair_info_header = f'<b>Buy ${token_symbol}</b> — ({token_name})\n'
    pair_info_body = f'Price: <b>${token_price}</b> — LIQ: <b>${formatted_liquidity}{liquidity_suffix}</b>\n5m: <b>{price_change_5_min}%</b> — 1h: <b>{price_change_1_hour}%</b> — 24h: <b>{price_change_24_hour}%</b>'

    # bot.send_message(chat_id, pair_info_header)
    bot.send_message(chat_id, pair_info_header + copy_token_address + pair_info_body, parse_mode='HTML') # formatting tap to copy
    # bot.send_message(chat_id, pair_info_body)

    # Creating Buttons 
    price_impact = calculate_price_impact()
    button_message = f'Price impact: {price_impact}%'

    #markup = buy_button_controller()
    markup = types.InlineKeyboardMarkup(row_width= 2)

    back_button = types.InlineKeyboardButton('Back', callback_data='buy_back_button')
    refresh_button = types.InlineKeyboardButton('Refresh', callback_data='buy_refresh_button')

    markup.add(back_button, refresh_button)

    bot.send_message(chat_id, button_message, reply_markup= markup)

# Calculating price impact
def calculate_price_impact():
    price_impact = 0 
    return price_impact

def buy_button_controller(message_id, chat_id):
    markup = types.InlineKeyboardMarkup(row_width= 2)

    back_button = types.InlineKeyboardButton('Back', callback_data='buy_back_button')
    refresh_button = types.InlineKeyboardButton('Refresh', callback_data='buy_refresh_button')

    markup.add(back_button, refresh_button)

    if message_id:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=data, reply_markup=markup)
    else:
        bot.send_message(chat_id, text=data, reply_markup=markup)


    return markup
# Creating solana wallet
def create_wallet():
    #
    mnemo = Mnemonic("english")
    my_words = mnemo.generate(256)
    seed_bytes = Bip39SeedGenerator(my_words).Generate() # generates a binary seed from the mnemonic phrase using the BIP39 seed generation process
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)

    # Get the private key bytes from the derived context
    private_key_bytes = bip44_chg_ctx.PrivateKey().Raw().ToBytes()

    # Create a Keypair from the private key bytes
    keypair = Keypair.from_seed(private_key_bytes[:32])
    
    return keypair

def get_account_balance(keypair):
    # Get the public key from the keypair
    account_pubkey = keypair.pubkey()  # Convert the pubkey to a string for the API call

    # Fetch the account balance
    balance_response: GetBalanceResp = SOLANA_CLIENT.get_balance(account_pubkey)
    print(balance_response)
    # Check if the request was successful
    if balance_response.value is not None:
        sol_balance = balance_response.value / 10**9  # Convert lamports to SOL
        # print(f"Account Balance: {sol_balance} SOL")
    else:
        sol_balance = "Failed to fetch the account balance."
    
    return sol_balance

def setting_page(message):
    markup = types.InlineKeyboardMarkup()

    buy_settings_button = types.InlineKeyboardButton('Buy Settings', callback_data='buy_settings_button')
    sell_settings_button = types.InlineKeyboardButton('Sell Settings', callback_data='sell_settings_button')

#Handling queries
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
     # 'call.data' contains the 'callback_data' from the inline button that was pressed
    if call.data == 'buy_button': # Buy button
        buy_command(call.message)
    elif call.data == 'buy_back_button': # Buy: Back button
        start_command(call.message)
    elif call.data == 'buy_refresh_button': # Buy: Refresh button
        print(call.message.text)
    elif call.data == 'settings_button':
        setting_page(call.message)


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



