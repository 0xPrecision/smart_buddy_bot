from telebot.types import Message
from config_data.bot_instance import bot


@bot.message_handler(func=lambda message: True)
def handle_unknown_command(message: Message) -> None:
    """
    Handler for unknown commands outside of an active dialog (FSM).
    
    Args:
    message (Message): User message.
	"""
    bot.send_message(
        message.chat.id,
        "❓ Неизвестная команда. Используй /help, чтобы посмотреть список доступных команд.",
    )
