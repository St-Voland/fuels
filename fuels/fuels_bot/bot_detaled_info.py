from .bot_common import *
from ..db.db_helper import get_nearest


def bot_detailed_info_message(context: CallbackContext):
    return "bot_detailed_info_message"

#find_station state
def bot_detailed_info(update: Update, context: CallbackContext) -> int:
    print("bot_detailed_info")
    
    i = int(update.callback_query.data[-1])

    input_range = context.user_data["input_location_range"]
    
    i += input_range[0]

    input_coords = context.user_data["input_location"]

    nearest_sorted = get_nearest(*input_coords)
    print(f"i  = {i} has been chosen")
    context.user_data["input_choice"] = i
    context.user_data["input_choice_data"] = nearest_sorted[i][0]

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=f"{nearest_sorted[i][0].address}")
    point = nearest_sorted[i][0].get_human_coordinates()
    lat, long = point.x, point.y
    update.callback_query.message.reply_location(latitude=lat, longitude=long)

    google_maps_link = "https://www.google.com/maps/dir/?api=1&" + \
        f"origin={context.user_data['input_location'][0]}%2C{context.user_data['input_location'][1]}&" + \
        f"destination={lat}%2C{long}&" + \
        "travelmode=car"
    
    if context.user_data.get(EUserType.USER, False):
        buttons = [
            [
                InlineKeyboardButton(text='Gmaps', url=f"{google_maps_link}"),
                InlineKeyboardButton(text='Back', callback_data=str(EStates.SHOW_STATIONS)),
                InlineKeyboardButton(text='Once again', callback_data=str(EStates.START_OVER)),
                InlineKeyboardButton(text='Close', callback_data=str(EStates.START)),
            ],
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        update.callback_query.message.reply_text(text = "Please, take a look", reply_markup=keyboard)
    elif context.user_data.get(EUserType.PROVIDER, False):
        buttons = [
            [
                InlineKeyboardButton(text='Gmaps', url=f"{google_maps_link}"),
                InlineKeyboardButton(text='Back', callback_data=str(EStates.SHOW_STATIONS)),
                InlineKeyboardButton(text='Once again', callback_data=str(EStates.START_OVER)),
                InlineKeyboardButton(text='Close', callback_data=str(EStates.START)),
            ],
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        update.callback_query.message.reply_text(text = "Please, take a look", reply_markup=keyboard)
        

    return EStates.SELECT_DETAILED_INFO
