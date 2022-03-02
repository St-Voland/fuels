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
from .data_parse import PharmaciesInfo
from ..utils import parse_coords
import numpy as np

import pickle
import pkg_resources
mocked_db_path = pkg_resources.resource_filename("fuels", "mock_data/cached_db.pkl")

with open(mocked_db_path, "rb") as f:
    mocked_db = pickle.load(f)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

class PharmacyBot:
    def __init__(self, creds="../TelegramBotCreds.json"):
        with open(creds) as f:
            self.telegram_bot_info = json.load(f)

            # verification integration will be done later!
            self.verified_users = []  # self.telegram_bot_info["verified_users"]
            self.blocked_users = []

            self.meters_in_geo = 75000  # approximately ))
            self.pharmacy_count = 5
            self.pharmacy_radius_in_meters = 2000  # 2 km radius

            self.set_messages()

            # self.pharmacies_info = PharmaciesInfo()
            # with open("cached_db.pkl", "wb") as f:
            #     pickle.dump(self.pharmacies_info, f)
            #     # mocked_db = pickle.load(f).get()
            self.pharmacies_info = mocked_db


    def set_messages(self):
        self.pharmacy_radius_in_meters_text = "Будь ласка, вкажіть який радіус у метрах вас влаштовує."
        self.pharmacy_count_text = "Будь ласка, вкажіть скільки аптек показати."

        self.pharmacy_message = f"Ось найближчі аптеки у радіусі {self.pharmacy_radius_in_meters} метрів."
        self.no_pharmacies_message = f"Більше немає аптек у радіусі {self.pharmacy_radius_in_meters}"

        self.help_message_text = "Будь ласка, надішліть свої дані локації для того щоб побачити найближчі аптеки!\n" +\
            "Напішіть '/count <x>' щоб бачити не більше <x> аптек(напр. /count 5)\n" +\
            "Напішіть '/radius <x>' щоб бачити аптеки лише у радіусі <x> метрів(напр. /radius 2000)\n" +\
            f"Наразі, ви будете бачити не більше {self.pharmacy_count} аптек у радіусі {self.pharmacy_radius_in_meters} метрів."
        self.start_message_text = "Слава Україні!\n" + self.help_message_text

    def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        update.message.reply_text(self.start_message_text)

    def help_command(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(self.help_message_text)

    def set_pharmacies_count(self, update: Update, context: CallbackContext) -> None:
        try:
            self.pharmacy_count = int(context.args[0])
            self.set_messages()
        except:
            logging.info(f"set_pharmacies_count failed")

    def set_pharmacies_radius(self, update: Update, context: CallbackContext) -> None:
        try:
            self.pharmacy_radius_in_meters = int(context.args[0])
            self.set_messages()
        except:
            logging.info(f"set_pharmacies_radius failed")

    def nearest_stations(self, update: Update, context: CallbackContext) -> None:
        """Echo the user message."""
        user = update.message.from_user

        # Use gmaps for visualization? Have no idea how they work. https://developers.google.com/maps/documentation/javascript/get-api-key

        # get data from site

        pharmacies_info = self.pharmacies_info.get()
        if update.message.location.latitude and update.message.location.longitude:
            input_coords = np.array([update.message.location.latitude, update.message.location.longitude])
        else:
            input_coords = np.array(parse_coords(update.message.text))

        nearest_sorted = sorted(pharmacies_info, key=lambda x: np.linalg.norm(x[2] - input_coords))
        nearest_count = self.pharmacy_count

        update.message.reply_text(self.pharmacy_message)
        for i in range(nearest_count):
            distance_in_meters = self.meters_in_geo * np.linalg.norm(nearest_sorted[i][2] - input_coords)
            if distance_in_meters < self.pharmacy_radius_in_meters:
                update.message.reply_text(f"<{nearest_sorted[i][0]}> за адресою <{nearest_sorted[i][1]}>:")
                update.message.reply_location(latitude=nearest_sorted[i][2][0], longitude=nearest_sorted[i][2][1])
            else:
                update.message.reply_text(self.no_pharmacies_message)
                break

        logger.info(f"user = {user}, with location = {update.message.location}")
        if update.message.from_user["id"] in self.blocked_users:
            # block functionality mock
            logger.info(f"user = {user} is blocked!")
            return

        if update.message.from_user["id"] in self.verified_users:
            # admin functionality mock
            logger.info(f"user = {user} is verified!")
            return

    def setup_pharmacy_bot(self, dispatcher):
        """Start the bot."""
        # updater = Updater(self.telegram_bot_info["token"], use_context=True)

        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.help_command))
        dispatcher.add_handler(CommandHandler("count", self.set_pharmacies_count))
        dispatcher.add_handler(CommandHandler("radius", self.set_pharmacies_radius))

        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.help_command))
        dispatcher.add_handler(MessageHandler(Filters.location, self.nearest_stations))
    
        # updater.start_polling()
        # updater.idle()


if __name__ == '__main__':
    bot = PharmacyBot()

    updater = Updater(bot.telegram_bot_info["token"], use_context=True)
    
    dispatcher = updater.dispatcher
    dispatcher = bot.setup_pharmacy_bot(dispatcher)

    updater.start_polling()
    updater.idle()
    

