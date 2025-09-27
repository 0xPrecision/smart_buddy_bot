from telebot.types import Message

from config_data.bot_instance import bot
from i18n.core import tr


@bot.message_handler(func=lambda message: True)
def handle_unknown_command(message: Message) -> None:
    """
    Handler for unknown commands outside of an active dialog (FSM).

    Args:
    message (Message): User message.
    """
    bot.send_message(
        message.chat.id,
        tr("unknown_command.messages.neizvestnaya-komanda-ispolzuj", ctx=message),
    )
