from telebot.types import Message

from config_data.bot_instance import bot
from i18n.core import tr
from states.state import pending_address, waiting_for_address
from utils.wait_timer import cancel_timer


@bot.message_handler(commands=["stop"])
def handle_stop(message: Message) -> None:
    """
    Handles the /stop command.
    Stops all pending user scenarios: resets waiting state,
    clears temporary data, stops the timer, and notifies the user of successful cancellation.

    Args:
    message (telebot.types.Message): Telegram message from the user.

    Notes:
    - If a process was active for the user (waiting for input), it is reset.
    - If no processes are active, the user receives the corresponding notification.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    in_dialog = False
    if waiting_for_address.pop(user_id, None) is not None:
        in_dialog = True
    if pending_address.pop(user_id, None) is not None:
        in_dialog = True
    cancel_timer(user_id)
    if in_dialog:
        bot.send_message(
            chat_id, tr("stop.messages.dejstvie-otmeneno-mozhesh-vybrat", ctx=message)
        )
    else:
        bot.send_message(
            chat_id, tr("stop.messages.sejchas-net-aktivnogo-dejstviya", ctx=message)
        )
