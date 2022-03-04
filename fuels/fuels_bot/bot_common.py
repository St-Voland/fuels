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
from ..utils import parse_coords

import numpy as np
from ..pharmacy_bot.data_parse import PharmaciesInfo # only for mocked db

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

from enum import Enum
class EStates(Enum):
    START = 0,
    END = 1,
    FIND_STATION = 2,
    ADD_STATION = 3,
    SHARE_LOCATION = 4,
    SHOW_STATIONS = 5,
    DETAILED_INFO = 6,
    FEEDBACK_FORM = 7,
    START_OVER = 8,
    SELECT_FIND_ADD_STATION = 9,
    SELECT_SEND_LOCATION_BACK = 10,
    SEND_LOCATION = 11,
    ASK_SEND_LOCATION = 12,
    SELECT_SHOW_STATIONS = 13,
    SHOW_STATIONS_NEXT = 14,
    SHOW_STATIONS_PREVIOUS = 15,
    SELECT_DETAILED_INFO = 16


class EUserType(Enum):
    UNKNOWN = "unknown",
    PROVIDER = "provider",
    USER = "user"
