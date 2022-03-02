
from dis import dis
from linecache import cache
import logging
from xml.dom.pulldom import START_DOCUMENT

# from telegram import Update  # , Location
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)



import json
from .utils import parse_coords
from .fuels_bot import bot_main_dispatcher
from .pharmacy_bot import PharmacyBot

import numpy as np
import pickle

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

from enum import Enum
class EBotType(Enum):
    Pharmacy = 0,
    Fuels = 1

class Bot:
    def __init__(self, creds="../TelegramBotCreds.json"):
        self.creds = creds
        with open(creds) as f:
            self.telegram_bot_info = json.load(f)

            # verification integration will be done later!
            self.bot_type = self.telegram_bot_info.get("bot_type", EBotType.Fuels)
            # self.bot_type = self.telegram_bot_info.get("bot_type", EBotType.Pharmacy)
            self.verified_users = [] 
            self.blocked_users = []

    def setup_pharmacy_bot(self):
        """Start the bot."""
        updater = Updater(self.telegram_bot_info["token"], use_context=True)

        dispatcher = updater.dispatcher
        self.pharmacy_bot = PharmacyBot(self.creds)

        dispatcher = self.pharmacy_bot.setup_pharmacy_bot(dispatcher)

        return updater

    def setup_fuels_bot(self):
        """Start the bot."""
        updater = Updater(self.telegram_bot_info["token"], use_context=True)

        dispatcher = updater.dispatcher
        dispatcher = bot_main_dispatcher(dispatcher)

        return updater
    
    def main(self):
        if self.bot_type == EBotType.Fuels:
            self.updater = self.setup_fuels_bot()
        elif self.bot_type == EBotType.Pharmacy:
            self.updater = self.setup_pharmacy_bot()
        
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    bot = Bot()
    bot.main()


