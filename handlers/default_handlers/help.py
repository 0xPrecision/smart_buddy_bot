from telebot.types import CallbackQuery, Message

from config_data.bot_instance import bot
from i18n.core import tr


@bot.message_handler(commands=["help"])
def send_help(message: Message) -> None:
    """
    Sends the user detailed help with bot commands and features.

    Args:
    message (telebot.types.Message): Incoming Telegram message from the user.
    """
    bot.send_message(
        message.chat.id,
        tr("help.messages.b-spravka-b-ya", ctx=message),
        parse_mode="HTML",
    )


@bot.callback_query_handler(func=lambda call: call.data == "help")
def callback_help(call: CallbackQuery) -> None:
    """
    Handles the press on the "Help" inline button, sending the user a help message.

    Args:
    call (telebot.types.CallbackQuery): Callback query from the user (button press).
    """
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        tr("help.messages.b-spravka-b-ya", ctx=call),
        parse_mode="HTML",
    )
