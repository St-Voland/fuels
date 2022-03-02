from fuels.fuels_bot.bot_add_station import bot_add_station
from .bot_common import *
from .bot_find_station import bot_find_station
from .bot_add_station import bot_add_station
from .bot_start import bot_start, bot_start_over
from .bot_stop import bot_stop
from .bot_send_location import bot_send_location
from .bot_ask_send_location import bot_ask_send_location
from .bot_detaled_info import bot_detailed_info
from .bot_show_stations import bot_show_stations, bot_show_stations_previous, bot_show_stations_next

def bot_main_dispatcher(dispatcher):
        # Set up top level ConversationHandler (selecting action)
    # Because the states of the third level conversation map to the ones of the second level
    # conversation, we need to make sure the top level conversation can also handle them
    selection_handlers = [
        CallbackQueryHandler(bot_start, pattern='^' + str(EStates.START) + '$'),
        CallbackQueryHandler(bot_find_station, pattern='^' + str(EStates.FIND_STATION) + '$'),
        CallbackQueryHandler(bot_add_station, pattern='^' + str(EStates.ADD_STATION) + '$'),
        CallbackQueryHandler(bot_ask_send_location, pattern='^' + str(EStates.ASK_SEND_LOCATION) + '$'),
        CallbackQueryHandler(bot_show_stations, pattern='^' + str(EStates.SHOW_STATIONS) + '$'),
        CallbackQueryHandler(bot_show_stations_previous, pattern='^' + str(EStates.SHOW_STATIONS_PREVIOUS) + '$'),
        CallbackQueryHandler(bot_show_stations_next, pattern='^' + str(EStates.SHOW_STATIONS_NEXT) + '$'),
        # CallbackQueryHandler(bot_stop, pattern='^' + str(EStates.END) + '$'),
        CallbackQueryHandler(bot_start, pattern='^' + str(EStates.START) + '$'),
        CallbackQueryHandler(bot_start_over, pattern='^' + str(EStates.START_OVER) + '$'),
        # CallbackQueryHandler(bot_show_stations, pattern='^' + str(EStates.SHOW_STATIONS) + '$'),
        # EStates.FIND_STATION: 
        # add_member_conv,
        # CallbackQueryHandler(show_data, pattern='^' + str(SHOWING) + '$'),
        # CallbackQueryHandler(adding_self, pattern='^' + str(ADDING_SELF) + '$'),
        # CallbackQueryHandler(end, pattern='^' + str(END) + '$'),
    ]

    for i in range(10):
        selection_handlers.append(CallbackQueryHandler(bot_detailed_info, pattern='^' + str(EStates.DETAILED_INFO) + str(i) + '$'),)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot_start)],
        states={
            EStates.SELECT_FIND_ADD_STATION: selection_handlers,
            EStates.SELECT_SEND_LOCATION_BACK: selection_handlers,
            EStates.SELECT_SHOW_STATIONS: selection_handlers,
            EStates.SELECT_DETAILED_INFO: selection_handlers,
            EStates.SHOW_STATIONS: selection_handlers,
            # EStates.SEND_LOCATION: [MessageHandler(Filters.location | Filters.text & ~Filters.command, bot_send_location)],
            # EStates.SEND_LOCATION: [MessageHandler(Filters.location, bot_send_location)],
            EStates.SEND_LOCATION: [MessageHandler(Filters.text & ~Filters.command, bot_send_location)],
            EStates.END: [CommandHandler('start', bot_start)]
        },
        fallbacks=[CommandHandler('stop', bot_stop)]
    )

    dispatcher.add_handler(conv_handler)
    return dispatcher
