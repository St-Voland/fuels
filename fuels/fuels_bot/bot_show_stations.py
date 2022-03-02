from .bot_common import *
import pickle

def bot_show_stations_message(context: CallbackContext):
    return "bot_show_stations_message"

#find_station state
def bot_show_stations(update: Update, context: CallbackContext) -> int:
    print("bot_show_stations")
    # update.callback_query.answer() #?

    input_coords = context.user_data["input_location"]
    input_radius = context.user_data["input_location_radius"]
    input_range = context.user_data["input_location_range"]
    input_range_step = context.user_data["input_location_range_step"]
    meters_in_geo = 75000

    nearest_sorted = sorted(mocked_db, key=lambda x: np.linalg.norm(x[2] - input_coords))
    buttons = []

    for i in range(input_range[0], input_range[1]):
        if i >= len(nearest_sorted):
            break
        distance_in_meters = meters_in_geo * np.linalg.norm(nearest_sorted[i][2] - input_coords)
        # if distance_in_meters >= input_radius:
        #     break

        button_name = f"{i}. {distance_in_meters} метрів, {nearest_sorted[i][1]}"
        buttons.append([InlineKeyboardButton(text = button_name, callback_data=str(EStates.DETAILED_INFO) + str(i - input_range[0]))])
    
    if input_range[0] > 0:
        button_name = f"Previous {input_range_step} stations"
        buttons.append([InlineKeyboardButton(text = button_name, callback_data=str(EStates.SHOW_STATIONS_PREVIOUS))])

    if len(buttons) == input_range[1] - input_range[0] and input_range[1] < len(nearest_sorted): #TODO: Ideally, we should also check that next element is close enough
        button_name = f"Next {input_range_step} stations"
        buttons.append([InlineKeyboardButton(text = button_name, callback_data=str(EStates.SHOW_STATIONS_NEXT))])
    
    buttons.append([InlineKeyboardButton(text = "Back", callback_data=str(EStates.ASK_SEND_LOCATION))])

    keyboard = InlineKeyboardMarkup(buttons)
    print(f"update = {update}")
    if getattr(update, "callback_query"):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text="Please, make your choice", reply_markup=keyboard)
    else:
        update.message.reply_text(text="Please, make your choice", reply_markup=keyboard)

    return EStates.SELECT_SHOW_STATIONS

def bot_show_stations_previous(update: Update, context: CallbackContext):
    input_range = context.user_data["input_location_range"]
    input_range_step = context.user_data["input_location_range_step"]
    context.user_data["input_location_range"] = (np.clip(input_range[0] - input_range_step, 0, input_range[0]), input_range[1] - input_range_step)
    if not context.user_data["input_location_range"][1] - context.user_data["input_location_range"][0] == input_range_step:
        context.user_data["input_location_range"] = context.user_data["input_location_range"][0], context.user_data["input_location_range"][0] + input_range_step

    return bot_show_stations(update, context)

def bot_show_stations_next(update: Update, context: CallbackContext):
    input_range = context.user_data["input_location_range"]
    input_range_step = context.user_data["input_location_range_step"]
    context.user_data["input_location_range"] = (input_range[0] + input_range_step, input_range[1] + input_range_step)
    return bot_show_stations(update, context)
