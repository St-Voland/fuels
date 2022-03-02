from .bot_common import *

def bot_find_station_message(context: CallbackContext):
    if context.user_data.get(EUserType.USER, False):
        return "bot_find_station_message for user"
    else:
        return "bot_find_station_message not for user"

#find_station state
def bot_find_station(update: Update, context: CallbackContext) -> int:
    print("bot_find_station")
    buttons = [
        [
            InlineKeyboardButton(text='Send location', callback_data=str(EStates.ASK_SEND_LOCATION)),
            InlineKeyboardButton(text='Back', callback_data=str(EStates.START_OVER))
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    
    context.user_data[EUserType.USER] = True
    context.user_data[EUserType.PROVIDER] = False

    # print(f"update = {update}")
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=bot_find_station_message(context), reply_markup=keyboard)

    return EStates.SELECT_SEND_LOCATION_BACK