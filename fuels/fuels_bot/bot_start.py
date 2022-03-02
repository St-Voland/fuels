from .bot_common import *
from .bot_stop import bot_stop

def bot_start_message(update: Update, context: CallbackContext, keyboard):
    if context.user_data.get(EStates.START_OVER, False):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text="bot_start_again", reply_markup=keyboard)
    else:
        update.message.reply_text(text="bot_start", reply_markup=keyboard)

#start state
def bot_start(update: Update, context: CallbackContext) -> int:
    bot_stop(update, context)
    buttons = [
        [
            InlineKeyboardButton(text='Provide info', callback_data=str(EStates.ADD_STATION)),
            InlineKeyboardButton(text='Use info', callback_data=str(EStates.FIND_STATION)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    bot_start_message(update, context, keyboard)

    context.user_data[EStates.START_OVER] = True

    return EStates.SELECT_FIND_ADD_STATION

#start state
def bot_start_over(update: Update, context: CallbackContext) -> int:
    buttons = [
        [
            InlineKeyboardButton(text='Provide info', callback_data=str(EStates.ADD_STATION)),
            InlineKeyboardButton(text='Use info', callback_data=str(EStates.FIND_STATION)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    bot_start_message(update, context, keyboard)

    context.user_data[EStates.START_OVER] = True

    return EStates.SELECT_FIND_ADD_STATION