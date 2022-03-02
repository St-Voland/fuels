from .bot_common import *

def bot_ask_send_location_message(context: CallbackContext):
    return "bot_ask_send_location_message"

#find_station state
def bot_ask_send_location(update: Update, context: CallbackContext) -> int:
    print("bot_ask_send_location")
    # update.callback_query.answer() #?
    # input_coords = np.array([update.message.location.latitude, update.message.location.longitude])
    # input_coords = update.message
    # print(f"{input_coords}")
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=f"{bot_ask_send_location_message(context)}")
    
    # update.message.reply_location(latitude=input_coords[0], longitude=input_coords[1])
    # update.message.reply_text(text=bot_send_location_message(context), reply_markup=keyboard)

    return EStates.SEND_LOCATION