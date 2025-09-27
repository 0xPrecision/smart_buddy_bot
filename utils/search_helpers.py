from telebot.types import Message

from config_data.bot_instance import bot
from i18n.core import tr
from states.state import waiting_for_address
from utils.bot_helpers import format_result, select_history
from utils.wait_timer import cancel_timer


def process_search_query(message: Message) -> None:
    """
    Handles a user request to search for an analysis by wallet address or nickname.
    Retrieves the analysis history and displays them one by one. If no history is found, informs the user.
    Ends the user's session.

    Args:
    message (Message): Telegram message object that initiated the search.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    state = waiting_for_address.get(user_id)
    if state == "search_query":
        analyses = select_history(message)
        analyses_count = analyses.count()
        if analyses_count:
            for analysis in analyses:
                bot.send_message(
                    chat_id,
                    format_result(analysis),
                    disable_web_page_preview=True,
                    parse_mode="HTML",
                )
        else:
            bot.send_message(
                chat_id,
                tr("search_helpers.messages.ne-udalos-najti-takoj", ctx=message),
            )
        waiting_for_address.pop(user_id, None)
        cancel_timer(user_id)
        bot.send_message(
            chat_id,
            tr("constants.messages.mozhesh-otpravit-novuyu-komandu", ctx=message),
        )
