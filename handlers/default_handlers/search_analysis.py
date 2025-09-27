from telebot.types import Message

from config_data.bot_instance import bot
from i18n.core import tr
from states.state import waiting_for_address
from utils.bot_helpers import on_timeout
from utils.misc.constants import TIMEOUT_SECONDS
from utils.wait_timer import start_waiting_timer


@bot.message_handler(commands=["search_analysis"])
def ask_for_address_or_nickname(message: Message) -> None:
    """
    Handles the /search_analysis command.
    Switches the user to the state of waiting for address or nickname input for analysis search.
    Starts a timeout timer.

    Args:
    message (telebot.types.Message): Telegram message from the user.

    Notes:
    - After this command, the bot waits for address or nickname input for analysis search.
    - If the user does not provide data within the allotted time, the on_timeout function will be called.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    waiting_for_address[user_id] = "search_query"
    bot.send_message(
        chat_id, tr("search_analysis.messages.prishli-adres-koshelka-ili", ctx=message)
    )
    start_waiting_timer(user_id, chat_id, TIMEOUT_SECONDS, on_timeout)
