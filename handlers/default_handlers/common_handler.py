from telebot.types import Message

from config_data.bot_instance import bot
from i18n.core import tr
from states.state import waiting_for_address
from utils.analysis_helpers import process_analyze_query, process_nickname
from utils.search_helpers import process_search_query


@bot.message_handler(func=lambda m: waiting_for_address.get(m.from_user.id))
def common_handler(message: Message) -> None:
    """
    FSM handler: processes all user messages in an active dialog (analysis, nickname input, search).
    If the user enters a command (starting with "/"), they receive a warning about the need to finish the dialog.

    Args:
    message (telebot.types.Message): Incoming user message.
    """
    user_id = message.from_user.id
    state = waiting_for_address.get(user_id)
    if message.text and message.text.startswith("/"):
        bot.send_message(
            message.chat.id,
            tr("common_handler.messages.pozhalujsta-zavershi-tekuschij", ctx=message),
        )
        return
    if state == "analyze_query":
        process_analyze_query(message)
    elif state == "nickname_query":
        process_nickname(message)
    elif state == "search_query":
        process_search_query(message)
