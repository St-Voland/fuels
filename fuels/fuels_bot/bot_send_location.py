from .bot_common import *
from .bot_show_stations import bot_show_stations
from .bot_stop import bot_stop

def bot_send_location_message(context: CallbackContext):
    return "bot_send_location_message"

#find_station state
def bot_send_location(update: Update, context: CallbackContext) -> int:
    print("bot_send_location")
    # update.callback_query.answer() #?
    if update.message.location:
        input_coords = np.array([update.message.location.latitude, update.message.location.longitude])
    else:
        input_coords = np.array([53, 48]) #update.message.text #TODO: parse!!!
    
    context.user_data["input_location"] = input_coords
    context.user_data["input_location_radius"] = 2000
    context.user_data["input_location_range"] = (0,10)
    context.user_data["input_location_range_step"] = 10

    return bot_show_stations(update, context)
