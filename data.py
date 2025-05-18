import telebot
from telebot import types
from typing import Final

class Token:
    def __init__(self) -> None:
        self.BOT_TOKEN: Final = ''
        self.BOT_USERNAME: Final = '@LeRegularBot'
        self.token_address: str = ''

    def get_bot_token(self) -> str:
        return self.BOT_TOKEN
    
    def get_bot_username(self) -> str:
        return  self.BOT_USERNAME
    
    def set_token_address(self, token_address: str) -> None:
        self.token_address = token_address

    # def clear_token_address(self) -> None:
    #     self.token_address = ''

    def get_token_address(self) -> str :
        return self.token_address
