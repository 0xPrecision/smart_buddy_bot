from telebot.types import Message
from config_data.bot_instance import bot
from utils.wait_timer import cancel_timer
from states.state import waiting_for_address, pending_address


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

    # Удаляем пользователя из состояния ожидания и временного хранилища
    if waiting_for_address.pop(user_id, None) is not None:
        in_dialog = True
    if pending_address.pop(user_id, None) is not None:
        in_dialog = True

    # Останавливаем связанный таймер (если он был запущен)
    cancel_timer(user_id)

    # Уведомляем пользователя о результате
    if in_dialog:
        bot.send_message(chat_id, "Действие отменено. Можешь выбрать новую команду.")
    else:
        bot.send_message(chat_id, "Сейчас нет активного действия для отмены.")
