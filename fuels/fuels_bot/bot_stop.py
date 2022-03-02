from .bot_common import *

def bot_stop_message(context: CallbackContext):
    return "bot_stop"

#stop state
def bot_stop(update: Update, context: CallbackContext) -> int:
    print(bot_stop_message(context))
    if getattr(update, "callback_query"):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=bot_stop_message(context))
    else:
        update.message.reply_text(text=bot_stop_message(context))

    if EStates.START_OVER in context.user_data:
        del context.user_data[EStates.START_OVER]

    if EUserType.PROVIDER in context.user_data:
        del context.user_data[EUserType.PROVIDER]

    if EUserType.USER in context.user_data:
        del context.user_data[EUserType.USER]

    return EStates.END
