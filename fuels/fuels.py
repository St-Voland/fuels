import logging

from telegram import Update #, Location
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import json

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

class FuelsBot:
    def __init__(self, creds = "../TelegramBotCreds.json"):
        with open(creds) as f:
            self.telegram_bot_info = json.load(f)
            self.verified_users = self.telegram_bot_info["verified_users"]
            self.blocked_users = []

    def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        update.message.reply_text('Слава Україні!')

    def help_command(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Будь ласка, надішліть свої дані локації для того щоб побачити найближчі заправки!')

    def nearest_stations(self, update: Update, context: CallbackContext) -> None:
        """Echo the user message."""
        # logic to get nearest_stations
        user = update.message.from_user

        # Use gmaps for visualization? Have no idea how they work. https://developers.google.com/maps/documentation/javascript/get-api-key

        update.message.reply_text('Ось найближча заправка з наявним пальним!')
        update.message.reply_location(latitude = update.message.location.latitude, longitude = update.message.location.longitude)
        
        logger.info(f"user = {user}, with location = {update.message.location}")
        if update.message.from_user["id"] in self.blocked_users:
            # block functionality mock
            logger.info(f"user = {user} is blocked!")
            return
        
        if update.message.from_user["id"] in self.verified_users:
            # admin functionality mock
            logger.info(f"user = {user} is verified!")
            return

    def main(self):
        """Start the bot."""
        updater = Updater(self.telegram_bot_info["token"], use_context=True)

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.help_command))

        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.help_command))
        dispatcher.add_handler(MessageHandler(Filters.location, self.nearest_stations))

        updater.start_polling()
        updater.idle()

if __name__ == '__main__':
    bot = FuelsBot()
    bot.main()
